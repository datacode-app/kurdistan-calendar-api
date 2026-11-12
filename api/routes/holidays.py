from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Optional
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Query, Request, Response

from api.core import data_store
from api.core.rate_limiter import DEFAULT_LIMIT, limiter

router = APIRouter(
    prefix="/api/v1/holidays",
    tags=["holidays"],
)

# "Today" is evaluated in Kurdistan Region local time, not server time
KURDISTAN_TZ = ZoneInfo("Asia/Baghdad")
LANG_PATTERN = "^(en|ku|ar|fa)$"


class Region(str, Enum):
    BASHUR = "bashur"
    BAKUR = "bakur"
    ROJHELAT = "rojhelat"
    ROJAVA = "rojava"
    ALL = "all"


class EventType(str, Enum):
    HISTORICAL = "historical"
    POLITICAL = "political"
    COMMEMORATION = "commemoration"
    CULTURAL = "cultural"
    RELIGIOUS = "religious"
    OFFICIAL = "official"


def today_in_kurdistan() -> date:
    return datetime.now(KURDISTAN_TZ).date()


def parse_date(value: str, name: str = "date") -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid {name} format. Use YYYY-MM-DD")


def select_events(
    years: Optional[List[int]] = None,
    include_historical: bool = False,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    is_holiday: Optional[bool] = None,
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
) -> List[dict]:
    """Load events and apply every filter. Results are sorted by date."""
    result = []
    for event in data_store.get_events(years, include_historical):
        try:
            event_date = date.fromisoformat(event["date"])
        except (KeyError, ValueError):
            continue
        if from_date and event_date < from_date:
            continue
        if to_date and event_date > to_date:
            continue
        if month and event_date.month != month:
            continue
        if day and event_date.day != day:
            continue
        if is_holiday is not None and bool(event.get("isHoliday")) != is_holiday:
            continue
        if region and region != Region.ALL:
            if str(event.get("region", "")).lower() not in (region.value, "all"):
                continue
        if type and event.get("type") != type.value:
            continue
        result.append(event)
    return result


def format_event(event: dict, lang: str) -> dict:
    names = event.get("event") or {}
    notes = event.get("note") or {}
    return {
        "date": event["date"],
        "kurdish_date": event.get("kurdish_date", {}),
        "isHoliday": bool(event.get("isHoliday", False)),
        "event": names.get(lang) or names.get("en", "Unknown"),
        "note": notes.get(lang) or notes.get("en") or None,
        "region": event.get("region", "unknown"),
        "type": event.get("type"),
        "tentative": bool(event.get("tentative", False)),
        "image": event.get("image"),
    }


def format_events(events: List[dict], lang: str) -> List[dict]:
    return [format_event(e, lang) for e in events]


@router.get("")
@limiter.limit(DEFAULT_LIMIT)
async def get_holidays(
    request: Request,
    year: Optional[int] = None,
    month: Optional[int] = Query(None, ge=1, le=12),
    day: Optional[int] = Query(None, ge=1, le=31),
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    lang: str = Query("en", pattern=LANG_PATTERN),
    is_holiday: Optional[bool] = None,
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
    include_historical: bool = False,
):
    """
    Get holidays and events with optional filters, sorted by date.

    - year / month / day: filter by Gregorian date component
    - from_date / to_date: inclusive range (YYYY-MM-DD)
    - lang: language for event and note fields (en, ku, ar, fa)
    - is_holiday: only official days off (true) or only observances (false)
    - region: bashur, bakur, rojhelat, rojava (events marked "all" always match)
    - type: historical, political, commemoration, cultural, religious, official
    - include_historical: include events from historical.json
    """
    events = select_events(
        years=[year] if year else None,
        include_historical=include_historical,
        from_date=parse_date(from_date, "from_date") if from_date else None,
        to_date=parse_date(to_date, "to_date") if to_date else None,
        month=month,
        day=day,
        is_holiday=is_holiday,
        region=region,
        type=type,
    )
    if year and include_historical:
        events = [e for e in events if e["date"].startswith(f"{year:04d}-")]
    return format_events(events, lang)


@router.get("/years")
@limiter.limit(DEFAULT_LIMIT)
async def get_years(request: Request):
    """List the years that have data, and whether each is official or projected."""
    return data_store.year_info()


@router.get("/today")
@limiter.limit(DEFAULT_LIMIT)
async def get_today_holidays(
    request: Request,
    lang: str = Query("en", pattern=LANG_PATTERN),
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
    include_historical: bool = False,
):
    """Get today's holidays and events (Kurdistan Region local time)."""
    today = today_in_kurdistan()
    events = select_events(
        years=[today.year], include_historical=include_historical,
        from_date=today, to_date=today, region=region, type=type,
    )
    return format_events(events, lang)


@router.get("/upcoming")
@limiter.limit(DEFAULT_LIMIT)
async def get_upcoming_holidays(
    request: Request,
    limit: int = Query(5, ge=1, le=50),
    lang: str = Query("en", pattern=LANG_PATTERN),
    is_holiday: Optional[bool] = None,
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
):
    """Get the next events from today onward (Kurdistan Region local time)."""
    events = select_events(
        from_date=today_in_kurdistan(), is_holiday=is_holiday, region=region, type=type,
    )
    return format_events(events[:limit], lang)


def _ics_escape(text: str) -> str:
    return (text.replace("\\", "\\\\").replace(";", "\\;")
            .replace(",", "\\,").replace("\n", "\\n"))


def _ics_fold(line: str) -> str:
    """Fold a content line to at most 75 octets, as required by RFC 5545."""
    chunks, current, size = [], "", 0
    for ch in line:
        width = len(ch.encode("utf-8"))
        if size + width > (75 if not chunks else 74):
            chunks.append(current)
            current, size = "", 0
        current += ch
        size += width
    chunks.append(current)
    return "\r\n ".join(chunks)


@router.get("/calendar.ics")
@limiter.limit(DEFAULT_LIMIT)
async def get_holidays_ics(
    request: Request,
    year: Optional[int] = None,
    lang: str = Query("en", pattern=LANG_PATTERN),
    is_holiday: Optional[bool] = None,
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
):
    """
    iCalendar feed that can be subscribed to from Google Calendar, Apple
    Calendar or Outlook. Accepts the same filters as the holidays list.
    """
    events = select_events(
        years=[year] if year else None, is_holiday=is_holiday, region=region, type=type,
    )
    stamp = datetime.now(ZoneInfo("UTC")).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Kurdistan Calendar API//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Kurdistan Calendar",
    ]
    counts = {}
    for raw in events:
        event = format_event(raw, lang)
        start = date.fromisoformat(event["date"])
        counts[event["date"]] = counts.get(event["date"], 0) + 1
        description = [event["kurdish_date"].get("full_date", "")]
        if event["note"]:
            description.append(event["note"])
        if event["tentative"]:
            description.append("Tentative date")
        lines += [
            "BEGIN:VEVENT",
            f"UID:{event['date']}-{counts[event['date']]}@kurdistan-calendar-api",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{start:%Y%m%d}",
            f"DTEND;VALUE=DATE:{start + timedelta(days=1):%Y%m%d}",
            f"SUMMARY:{_ics_escape(event['event'])}",
            f"DESCRIPTION:{_ics_escape(chr(10).join(d for d in description if d))}",
            f"CATEGORIES:{'Holiday' if event['isHoliday'] else 'Observance'}",
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    body = "\r\n".join(_ics_fold(line) for line in lines) + "\r\n"
    return Response(
        content=body,
        media_type="text/calendar; charset=utf-8",
        headers={"Content-Disposition": 'inline; filename="kurdistan-calendar.ics"'},
    )


@router.get("/range/{from_date}/{to_date}")
@limiter.limit(DEFAULT_LIMIT)
async def get_holidays_by_date_range(
    request: Request,
    from_date: str,
    to_date: str,
    lang: str = Query("en", pattern=LANG_PATTERN),
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
    is_holiday: Optional[bool] = None,
    include_historical: bool = False,
):
    """
    Get holidays within an inclusive date range (YYYY-MM-DD).
    Historical events are included automatically when the range starts
    before the first year file.
    """
    start = parse_date(from_date, "from_date")
    end = parse_date(to_date, "to_date")
    if end < start:
        raise HTTPException(status_code=400, detail="End date must be on or after start date")

    years = data_store.available_years()
    before_data = bool(years) and start.year < years[0]
    events = select_events(
        years=[y for y in years if start.year <= y <= end.year],
        include_historical=include_historical or before_data,
        from_date=start, to_date=end,
        region=region, type=type, is_holiday=is_holiday,
    )
    return format_events(events, lang)


@router.get("/{date}")
@limiter.limit(DEFAULT_LIMIT)
async def get_holidays_by_date(
    request: Request,
    date: str,
    lang: str = Query("en", pattern=LANG_PATTERN),
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
    include_historical: bool = False,
):
    """Get holidays for a specific date (YYYY-MM-DD)."""
    target = parse_date(date)
    events = select_events(
        years=[target.year], include_historical=include_historical,
        from_date=target, to_date=target, region=region, type=type,
    )
    return format_events(events, lang)
