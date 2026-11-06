import os
import re
import sys
from pathlib import Path


def app_dir() -> Path:
    """Folder that holds user-facing files: config, user presets, log, assets/masks.

    Frozen exe: the folder containing SpriteGibber.exe (not PyInstaller's
    _internal/ extraction dir, which is where __file__ points when frozen).
    From source: the project root.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def app_path(*parts) -> Path:
    return app_dir().joinpath(*parts)


def resolve_user_path(raw: str) -> str:
    """Absolute paths pass through; relative ones are taken relative to app_dir()."""
    if os.path.isabs(raw):
        return raw
    return str(app_dir() / raw)


def masks_dir() -> Path:
    return app_path("assets", "masks")


# Default export destination: a subfolder next to each sprite.
EXPORT_SUBFOLDER = "gibbed"


def normalize_user_file(raw) -> str:
    """Absolute, normalised form used to store user-picked files (the sprite list)."""
    return os.path.normpath(os.path.abspath(resolve_user_path(str(raw))))


def same_path(a: str, b: str) -> bool:
    return os.path.normcase(os.path.normpath(a)) == os.path.normcase(os.path.normpath(b))


def _natural_key(name: str):
    """Sort 'sprite (2)' before 'sprite (10)'."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def list_pngs(folder) -> list:
    """PNG files directly inside folder (subfolders are ignored), natural-sorted.

    Raises OSError if the folder can't be read.
    """
    folder = normalize_user_file(folder)
    names = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
    paths = [os.path.join(folder, f) for f in sorted(names, key=_natural_key)]
    return [p for p in paths if os.path.isfile(p)]


def export_dir_for(sprite_path: str, dest_mode: str, dest_folder) -> str:
    """Folder that receives <stem>/ for one sprite.

    dest_mode "folder" with a chosen folder → that folder; anything else →
    a gibbed/ subfolder next to the sprite.
    """
    if dest_mode == "folder" and dest_folder:
        return resolve_user_path(dest_folder)
    return os.path.join(os.path.dirname(sprite_path), EXPORT_SUBFOLDER)


def write_text_atomic(path, text: str, newline=None) -> None:
    """Write via a temp file + os.replace so a crash mid-write can't truncate the target.

    newline: passed to open(); "" writes the text's line endings verbatim.
    """
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline=newline) as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def quarantine_corrupt(path) -> Path:
    """Rename an unreadable file aside (…corrupt-N.json) so the next save can't overwrite it."""
    path = Path(path)
    n = 1
    while True:
        dest = path.with_name(f"{path.stem}.corrupt-{n}{path.suffix}")
        if not dest.exists():
            break
        n += 1
    os.replace(path, dest)
    return dest
