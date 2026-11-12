#!/usr/bin/env python3
"""
Validate the data files in data/years.

Checks the schema of every entry (required fields, languages, region, type),
that entries sit in the right year file and are free of duplicates, and that
the stored Kurdish date matches the Gregorian date.

    python scripts/validate_data.py          # validate, exit 1 on errors
    python scripts/validate_data.py --fix    # rewrite kurdish_date + sort entries
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from api.utils.date_utils import gregorian_to_kurdish  # noqa: E402

DATA_DIR = ROOT / "data" / "years"
LANGS = ("en", "ku", "ar", "fa")
REGIONS = {"bashur", "bakur", "rojhelat", "rojava", "all"}
TYPES = {"historical", "political", "commemoration", "cultural", "religious", "official"}
STATUSES = {"official", "projected"}


def validate_file(path: Path) -> List[str]:
    errors: List[str] = []

    def err(message: str) -> None:
        errors.append(f"{path.name}: {message}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name}: invalid JSON ({exc})"]
    if not isinstance(data, dict) or not isinstance(data.get("holidays"), list):
        return [f"{path.name}: root must be an object with a 'holidays' list"]

    file_year = int(path.stem) if path.stem.isdigit() else None
    if file_year:
        if data.get("year") != file_year:
            err(f"'year' must be {file_year}")
        if data.get("status") not in STATUSES:
            err(f"'status' must be one of {sorted(STATUSES)}")

    seen = set()
    previous = ""
    for index, entry in enumerate(data["holidays"]):
        where = f"entry {index} ({entry.get('date', '?')})"
        try:
            parsed = date.fromisoformat(entry["date"])
        except (KeyError, TypeError, ValueError):
            err(f"{where}: 'date' must be YYYY-MM-DD")
            continue
        if file_year and parsed.year != file_year:
            err(f"{where}: does not belong in {path.name}")
        if entry["date"] < previous:
            err(f"{where}: entries must be sorted by date")
        previous = entry["date"]

        if not isinstance(entry.get("isHoliday"), bool):
            err(f"{where}: 'isHoliday' must be true or false")
        if entry.get("region") not in REGIONS:
            err(f"{where}: 'region' must be one of {sorted(REGIONS)}")
        if entry.get("type") not in TYPES:
            err(f"{where}: 'type' must be one of {sorted(TYPES)}")
        if "tentative" in entry and not isinstance(entry["tentative"], bool):
            err(f"{where}: 'tentative' must be true or false")

        names = entry.get("event")
        if not isinstance(names, dict) or any(not names.get(lang) for lang in LANGS):
            err(f"{where}: 'event' needs a non-empty name in {', '.join(LANGS)}")
        else:
            key = (entry["date"], names["en"])
            if key in seen:
                err(f"{where}: duplicate of '{names['en']}'")
            seen.add(key)
        note = entry.get("note")
        if note is not None and (not isinstance(note, dict) or any(not note.get(lang) for lang in LANGS)):
            err(f"{where}: 'note', when present, needs text in {', '.join(LANGS)}")

        expected = gregorian_to_kurdish(parsed)
        if entry.get("kurdish_date") != expected:
            err(f"{where}: kurdish_date should be {expected['full_date_latin']} (run with --fix)")
    return errors


def fix_file(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    for entry in data["holidays"]:
        entry["kurdish_date"] = gregorian_to_kurdish(entry["date"])
    data["holidays"].sort(key=lambda e: e["date"])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_all() -> List[str]:
    errors: List[str] = []
    for path in sorted(DATA_DIR.glob("*.json")):
        errors.extend(validate_file(path))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--fix", action="store_true", help="recompute kurdish_date and sort entries")
    args = parser.parse_args()

    if args.fix:
        for path in sorted(DATA_DIR.glob("*.json")):
            fix_file(path)
    errors = validate_all()
    for message in errors:
        print(f"ERROR: {message}")
    print(f"{len(list(DATA_DIR.glob('*.json')))} files checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
