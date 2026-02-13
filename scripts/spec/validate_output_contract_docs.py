from pathlib import Path


def command_docs() -> list[Path]:
    root = Path(__file__).resolve().parents[2]
    return sorted((root / "aria" / "commands").glob("*.md"))


if __name__ == "__main__":
    docs = command_docs()
    print(f"Found {len(docs)} command docs.")
