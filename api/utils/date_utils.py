"""
Kurdish calendar conversion utilities.

Convention used by this project (the "fixed Newroz" Kurdish solar calendar):

* The year starts on Newroz, 21 March (1 Xakelew).
* Kurdish year = Gregorian year + 700 from 21 March onward, + 699 before it.
* Months 1-6 have 31 days, months 7-11 have 30 days, and the last month
  (Reşeme) has 29 days, or 30 when it contains a Gregorian 29 February.

Because the year is anchored to 21 March, every date converts with plain
arithmetic and the conversion is an exact, lossless round trip.
"""

from datetime import date, datetime, timedelta
from typing import Dict, Union

YEAR_OFFSET = 700
NEWROZ_MONTH, NEWROZ_DAY = 3, 21

# Latin month names (kept stable: they are part of the public API)
KURDISH_MONTHS = {
    1: "Xakelew",    # March/April
    2: "Gullan",     # April/May
    3: "Cozerdan",   # May/June
    4: "Pûşper",     # June/July
    5: "Gelawêj",    # July/August
    6: "Xermanan",   # August/September
    7: "Rezber",     # September/October
    8: "Gelarêzan",  # October/November
    9: "Sermawez",   # November/December
    10: "Befranbar", # December/January
    11: "Rêbendan",  # January/February
    12: "Reşeme",    # February/March
}

# Sorani (Arabic script) month names
KURDISH_MONTHS_SORANI = {
    1: "خاکەلێوە",
    2: "گوڵان",
    3: "جۆزەردان",
    4: "پووشپەڕ",
    5: "گەلاوێژ",
    6: "خەرمانان",
    7: "ڕەزبەر",
    8: "گەڵاڕێزان",
    9: "سەرماوەز",
    10: "بەفرانبار",
    11: "ڕێبەندان",
    12: "ڕەشەمە",
}

# Gregorian (month, day) on which each Kurdish month starts
MONTH_START_DAYS = {
    "Xakelew": (3, 21),
    "Gullan": (4, 21),
    "Cozerdan": (5, 22),
    "Pûşper": (6, 22),
    "Gelawêj": (7, 23),
    "Xermanan": (8, 23),
    "Rezber": (9, 23),
    "Gelarêzan": (10, 23),
    "Sermawez": (11, 22),
    "Befranbar": (12, 22),
    "Rêbendan": (1, 21),
    "Reşeme": (2, 20),
}

KURDISH_NUMERALS = {
    '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
    '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
}

_MONTH_LOOKUP = {}
for _num, _name in KURDISH_MONTHS.items():
    _MONTH_LOOKUP[_name.lower()] = _num
for _num, _name in KURDISH_MONTHS_SORANI.items():
    _MONTH_LOOKUP[_name] = _num


def _to_date(value: Union[str, date, datetime]) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(value[:10])


def _newroz(kurdish_year: int) -> date:
    """Gregorian date of 1 Xakelew for the given Kurdish year."""
    return date(kurdish_year - YEAR_OFFSET, NEWROZ_MONTH, NEWROZ_DAY)


def month_number(month: Union[str, int]) -> int:
    """Resolve a month given as a number, numeric string, Latin or Sorani name."""
    if isinstance(month, int):
        number = month
    else:
        text = str(month).strip()
        if text.isdigit():
            number = int(text)
        else:
            number = _MONTH_LOOKUP.get(text.lower()) or _MONTH_LOOKUP.get(text)
            if number is None:
                raise ValueError(f"Invalid Kurdish month name: {month}")
    if not 1 <= number <= 12:
        raise ValueError(f"Invalid Kurdish month number: {number}")
    return number


def days_in_kurdish_year(kurdish_year: int) -> int:
    return (_newroz(kurdish_year + 1) - _newroz(kurdish_year)).days


def days_in_kurdish_month(kurdish_year: int, month: Union[str, int]) -> int:
    number = month_number(month)
    if number <= 6:
        return 31
    if number <= 11:
        return 30
    return days_in_kurdish_year(kurdish_year) - 336


def to_kurdish_numerals(value: Union[int, str]) -> str:
    return ''.join(KURDISH_NUMERALS.get(ch, ch) for ch in str(value))


def format_kurdish_date(day: int, month: Union[str, int], year: int) -> str:
    """Format a Kurdish date in Sorani, e.g. "١ی خاکەلێوە ٢٧٢٦"."""
    name = KURDISH_MONTHS_SORANI[month_number(month)]
    return f"{to_kurdish_numerals(day)}ی {name} {to_kurdish_numerals(year)}"


def gregorian_to_kurdish(gregorian_date: Union[str, date, datetime]) -> Dict[str, Union[int, str]]:
    """
    Convert a Gregorian date ('YYYY-MM-DD', date or datetime) to a Kurdish date.

    Returns year, month (Latin name), month_number, month_ku (Sorani name),
    day, full_date (Sorani) and full_date_latin.
    """
    greg = _to_date(gregorian_date)

    kurdish_year = greg.year + YEAR_OFFSET
    if greg < _newroz(kurdish_year):
        kurdish_year -= 1

    remaining = (greg - _newroz(kurdish_year)).days
    number = 1
    while remaining >= days_in_kurdish_month(kurdish_year, number):
        remaining -= days_in_kurdish_month(kurdish_year, number)
        number += 1
    day = remaining + 1

    return {
        "year": kurdish_year,
        "month": KURDISH_MONTHS[number],
        "month_number": number,
        "month_ku": KURDISH_MONTHS_SORANI[number],
        "day": day,
        "full_date": format_kurdish_date(day, number, kurdish_year),
        "full_date_latin": f"{day} {KURDISH_MONTHS[number]} {kurdish_year}",
    }


def is_valid_kurdish_date(kurdish_year: int, kurdish_month: Union[str, int], kurdish_day: int) -> bool:
    try:
        number = month_number(kurdish_month)
        # Gregorian year must stay inside what datetime.date supports
        if not 701 <= kurdish_year <= 10698:
            return False
        return 1 <= kurdish_day <= days_in_kurdish_month(kurdish_year, number)
    except (ValueError, TypeError):
        return False


def kurdish_to_gregorian(kurdish_year: int, kurdish_month: Union[str, int], kurdish_day: int) -> str:
    """Convert a Kurdish date to a Gregorian date string (YYYY-MM-DD)."""
    number = month_number(kurdish_month)
    if not is_valid_kurdish_date(kurdish_year, number, kurdish_day):
        raise ValueError(
            f"Invalid Kurdish date: {kurdish_year}-{number}-{kurdish_day}"
        )
    offset = sum(days_in_kurdish_month(kurdish_year, m) for m in range(1, number))
    return (_newroz(kurdish_year) + timedelta(days=offset + kurdish_day - 1)).isoformat()
