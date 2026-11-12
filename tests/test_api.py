from datetime import date

from api.routes import holidays as holidays_route

BASE = "/api/v1/holidays"


def test_root(client):
    assert client.get("/").json()["name"] == "Kurdistan Calendar API"


def test_year_is_sorted_and_keeps_same_day_events(client):
    data = client.get(f"{BASE}?year=2026").json()
    dates = [h["date"] for h in data]
    assert dates == sorted(dates)
    # Three different events share 21 March 2026; none may be dropped
    assert len([h for h in data if h["date"] == "2026-03-21"]) == 3
    assert all(d.startswith("2026-") for d in dates)


def test_years_listing(client):
    years = {y["year"]: y for y in client.get(f"{BASE}/years").json()}
    assert years[2026]["status"] == "official"
    assert years[2027]["status"] == "projected"


def test_newroz_2026(client):
    data = client.get(f"{BASE}/2026-03-21?type=cultural").json()
    assert len(data) == 1
    assert data[0]["isHoliday"] is True
    assert data[0]["kurdish_date"]["year"] == 2726
    assert data[0]["kurdish_date"]["day"] == 1


def test_language(client):
    data = client.get(f"{BASE}/2026-03-16?lang=ku").json()
    assert data[0]["event"] == "یادی کیمیابارانی هەڵەبجە"
    assert client.get(f"{BASE}?lang=xx").status_code == 422


def test_filters(client):
    days_off = client.get(f"{BASE}?year=2026&is_holiday=true").json()
    assert days_off and all(h["isHoliday"] for h in days_off)
    religious = client.get(f"{BASE}?year=2026&type=religious").json()
    assert religious and all(h["type"] == "religious" for h in religious)
    rojava = client.get(f"{BASE}?year=2026&region=rojava").json()
    assert rojava and all(h["region"] in ("rojava", "all") for h in rojava)
    march = client.get(f"{BASE}?year=2026&month=3").json()
    assert march and all(h["date"][5:7] == "03" for h in march)


def test_tentative_flag(client):
    data = client.get(f"{BASE}/2027-03-09").json()
    assert data[0]["tentative"] is True
    assert client.get(f"{BASE}/2026-03-20").json()[0]["tentative"] is False


def test_range(client):
    data = client.get(f"{BASE}/range/2025-12-01/2026-01-31").json()
    dates = [h["date"] for h in data]
    assert dates == sorted(dates)
    assert "2025-12-25" in dates and "2026-01-01" in dates
    assert all("2025-12-01" <= d <= "2026-01-31" for d in dates)


def test_range_before_first_year_includes_historical(client):
    data = client.get(f"{BASE}/range/1988-01-01/1988-12-31").json()
    assert [h["date"] for h in data] == ["1988-03-16"]


def test_bad_input_returns_400(client):
    assert client.get(f"{BASE}/not-a-date").status_code == 400
    assert client.get(f"{BASE}/range/2026-02-01/2026-01-01").status_code == 400
    assert client.get(f"{BASE}?from_date=2026-13-01").status_code == 400


def test_today_and_upcoming(client, monkeypatch):
    monkeypatch.setattr(holidays_route, "today_in_kurdistan", lambda: date(2026, 12, 17))
    today = client.get(f"{BASE}/today").json()
    assert [h["event"] for h in today] == ["Kurdistan Flag Day"]
    upcoming = client.get(f"{BASE}/upcoming?limit=3&is_holiday=true").json()
    assert [h["date"] for h in upcoming] == ["2026-12-25", "2027-01-01", "2027-03-05"]


def test_ics(client):
    res = client.get(f"{BASE}/calendar.ics?year=2026&is_holiday=true")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/calendar")
    body = res.text
    assert body.startswith("BEGIN:VCALENDAR\r\n") and body.endswith("END:VCALENDAR\r\n")
    assert "DTSTART;VALUE=DATE:20260321" in body
    assert body.count("BEGIN:VEVENT") == body.count("END:VEVENT") > 20
    assert all(len(line.encode()) <= 75 for line in body.split("\r\n"))
    uids = [line for line in body.split("\r\n") if line.startswith("UID:")]
    assert len(uids) == len(set(uids))


def test_conversion_endpoints(client):
    cal = "/api/v1/calendar"
    res = client.get(f"{cal}/convert/gregorian-to-kurdish/2026-03-21").json()
    assert res["kurdish_date"]["full_date_latin"] == "1 Xakelew 2726"
    res = client.post(f"{cal}/convert/kurdish-to-gregorian", json={"year": 2726, "month": "Xakelew", "day": 1})
    assert res.json()["gregorian_date"] == "2026-03-21"
    res = client.post(f"{cal}/convert/kurdish-to-gregorian", json={"year": 2726, "month": 7, "day": 31})
    assert res.status_code == 400
    assert client.get(f"{cal}/convert/gregorian-to-kurdish/nope").status_code == 400
    assert client.get(f"{cal}/validate/kurdish-date?year=2723&month=12&day=30").json()["is_valid"] is True
    assert client.get(f"{cal}/validate/kurdish-date?year=2725&month=Reşeme&day=30").json()["is_valid"] is False
    assert "kurdish_date" in client.get(f"{cal}/today").json()


def test_rate_limit_is_enforced(client):
    from api.core.rate_limiter import DEFAULT_LIMIT, limiter
    allowed = int(DEFAULT_LIMIT.split("/")[0])
    limiter.reset()
    limiter.enabled = True
    try:
        codes = [client.get(f"{BASE}/years").status_code for _ in range(allowed + 1)]
    finally:
        limiter.enabled = False
        limiter.reset()
    assert codes[:allowed] == [200] * allowed
    assert codes[-1] == 429
