"""Check every catalog file against the schema.

Usage:
    python src/validate_catalogs.py data/catalogs
    python src/validate_catalogs.py data/bad_examples
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "catalog.schema.json"


def validate_folder(folder: Path) -> int:
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft202012Validator(schema)
    problems = 0
    for path in sorted(folder.glob("*.json")):
        data = json.loads(path.read_text())
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if not errors:
            print(f"OK    {path.name}")
            continue
        problems += 1
        print(f"FAIL  {path.name}")
        for err in errors:
            where = "/".join(str(p) for p in err.path) or "(top level)"
            print(f"        at {where}: {err.message}")
    return problems


if __name__ == "__main__":
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/catalogs")
    sys.exit(1 if validate_folder(folder) else 0)
