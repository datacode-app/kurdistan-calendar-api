from datetime import date, timedelta

import pytest

from api.utils.date_utils import (
    days_in_kurdish_month,
    gregorian_to_kurdish,
    is_valid_kurdish_date,
    kurdish_to_gregorian,
)


@pytest.mark.parametrize("greg, year, month, day", [
    ("2026-03-21", 2726, "Xakelew", 1),
    ("2026-03-20", 2725, "Reşeme", 29),
    ("2024-03-20", 2723, "Reşeme", 30),   # leap year
    ("2024-03-05", 2723, "Reşeme", 15),
    ("2025-03-05", 2724, "Reşeme", 14),
    ("2026-01-01", 2725, "Befranbar", 11),
    ("2026-09-22", 2726, "Xermanan", 31),
    ("2026-09-23", 2726, "Rezber", 1),
    ("2026-12-25", 2726, "Befranbar", 4),
    ("1988-03-16", 2687, "Reşeme", 26),
])
def test_known_dates(greg, year, month, day):
    k = gregorian_to_kurdish(greg)
    assert (k["year"], k["month"], k["day"]) == (year, month, day)
    assert kurdish_to_gregorian(year, month, day) == greg


def test_round_trip_every_day():
    d = date(1990, 1, 1)
    while d < date(2040, 1, 1):
        k = gregorian_to_kurdish(d)
        assert 1 <= k["day"] <= days_in_kurdish_month(k["year"], k["month_number"])
        assert kurdish_to_gregorian(k["year"], k["month_number"], k["day"]) == d.isoformat()
        d += timedelta(days=1)


def test_formatting():
    k = gregorian_to_kurdish("2026-03-21")
    assert k["full_date"] == "١ی خاکەلێوە ٢٧٢٦"
    assert k["full_date_latin"] == "1 Xakelew 2726"
    assert k["month_ku"] == "خاکەلێوە"


def test_validation():
    assert is_valid_kurdish_date(2726, "Xakelew", 31)
    assert not is_valid_kurdish_date(2726, "Xakelew", 32)
    assert not is_valid_kurdish_date(2726, "Rezber", 31)
    assert is_valid_kurdish_date(2723, 12, 30)        # leap
    assert not is_valid_kurdish_date(2725, 12, 30)    # not leap
    assert not is_valid_kurdish_date(2726, "NotAMonth", 1)
    assert not is_valid_kurdish_date(2726, 13, 1)
    assert is_valid_kurdish_date(2726, "خاکەلێوە", 1)
    with pytest.raises(ValueError):
        kurdish_to_gregorian(2725, 12, 30)
