import sys
from sqlmodel import SQLModel

from ingestion import run_ingestion
from run_rules import run_apply
from db.engine import engine

def main():
    if len(sys.argv) != 2:
        print("Usage: uv run main.py [ingestion|apply]")
        return
    SQLModel.metadata.create_all(engine)
    command = sys.argv[1].lower()
    if command == "ingestion":
        run_ingestion(engine)
    elif command == "apply":
        run_apply(engine)
    else:
        print("Invalid argument. Use 'ingestion' or 'apply'.")


if __name__ == "__main__":
    main()
