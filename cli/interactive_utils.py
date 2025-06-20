from pathlib import Path

import questionary


def get_directory_choices(current_path: Path, root_path: Path) -> list[str]:
    choices = []

    if current_path != root_path:
        choices.append(".. (go up)")

    for entry in sorted(current_path.iterdir()):
        if entry.is_dir():
            choices.append(f"[DIR] {entry.name}")
        elif entry.suffix == ".json":
            choices.append(entry.name)

    return choices


def select_option(current_path: Path, choices: list[str]) -> str | None:
    return questionary.select(
        f"📂 Current directory: {current_path}", choices=choices
    ).ask()


def select_snapshot_file(start_path: str = "data/snapshots") -> str | None:
    root_path = Path(start_path).resolve()
    current_path = root_path

    while True:
        if not current_path.exists():
            print(f"❌ Path not found: {current_path}")
            return None

        choices = get_directory_choices(current_path, root_path)

        if not choices:
            print("📁 No selectable files or folders found here.")
            return None

        selected = select_option(current_path, choices)
        if selected is None:
            return None

        if selected == ".. (go up)":
            current_path = current_path.parent
        else:
            selected_path = current_path / selected.lstrip("[DIR] ").strip()
            if selected_path.is_dir():
                current_path = selected_path
            elif selected_path.is_file():
                return str(selected_path)
