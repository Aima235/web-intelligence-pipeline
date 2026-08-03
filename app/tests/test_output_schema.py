import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

sys.path.insert(0, PROJECT_ROOT)

print("Project Root:", PROJECT_ROOT)
print("Python Path:", sys.path[0])

from schemas.output_schema import create_output_schema
from utils.schema_validator import validate_schema


def main():
    schema = create_output_schema()

    missing = validate_schema(schema)

    if missing:
        print("Missing Fields:", missing)
    else:
        print("✓ Schema validation passed.")


if __name__ == "__main__":
    main()