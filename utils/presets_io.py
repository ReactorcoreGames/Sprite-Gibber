import ast
import json

from utils.config import _config_path, read_json_file, DEFAULT_CONFIG, GUI_ONLY_KEYS
from utils.log import log
from utils.paths import write_text_atomic

# Official presets live in presets/*.py and are read-only in the app; their names
# start with "*". Custom presets live in user_presets.json and never start with "*",
# so the two can't collide and an official original can never be shadowed or lost.
OFFICIAL_PREFIX = "*"

# Characters Windows forbids in file names — preset names end up in export file names.
_ILLEGAL_NAME_CHARS = '<>:"/\\|?*'
_MAX_NAME_LEN = 80


def is_official_name(name: str) -> bool:
    return bool(name) and name.startswith(OFFICIAL_PREFIX)


def display_stem(name: str) -> str:
    """Preset name without the official '*.' marker, e.g. '*.Fire-Burn-terra' → 'Fire-Burn-terra'."""
    return name.lstrip("*").lstrip(".") if is_official_name(name) else name


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _params_to_save(config: dict) -> dict:
    """Return only engine params that differ from their default value.

    Strips GUI-only keys and any key not in DEFAULT_CONFIG (e.g. rand_ flags),
    then diffs against defaults so saved presets stay lean.
    """
    return {
        k: config[k]
        for k in config
        if k not in GUI_ONLY_KEYS
        and k in DEFAULT_CONFIG
        and config[k] != DEFAULT_CONFIG[k]
    }


def preset_effect_config(params: dict) -> dict:
    """The full set of effect params a preset produces: defaults overlaid with its params."""
    out = {k: v for k, v in DEFAULT_CONFIG.items() if k not in GUI_ONLY_KEYS}
    out.update({k: v for k, v in params.items() if k not in GUI_ONLY_KEYS})
    return out


def _values_differ(a, b) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
            and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(a - b) > 1e-9
    return a != b


def is_modified(config: dict, name) -> bool:
    """True if the current settings differ from what preset `name` loads."""
    entry = get_preset(name) if name else None
    if entry is None:
        return False
    target = preset_effect_config(entry.get("params", {}))
    return any(_values_differ(config.get(k), v) for k, v in target.items())


def get_preset(name: str):
    """Look up a preset by name — official (presets/*.py) or custom (user_presets.json)."""
    import presets
    if is_official_name(name):
        return presets.PRESETS.get(name)
    for e in load_user_presets():
        if e["name"] == name:
            return e
    return None


# ---------------------------------------------------------------------------
# Custom preset I/O
# ---------------------------------------------------------------------------

_user_cache = None  # list of custom entries; invalidated on every write


def _user_presets_path():
    return _config_path("user_presets.json")


def load_user_presets() -> list:
    global _user_cache
    if _user_cache is None:
        entries = []
        for e in read_json_file(_user_presets_path(), list) or []:
            if not (isinstance(e, dict) and isinstance(e.get("name"), str)
                    and isinstance(e.get("params"), dict)):
                log.warning("Skipping malformed custom preset entry: %r", e)
                continue
            if is_official_name(e["name"]):
                # Pre-B2 files stored edits of official presets under the official
                # name. Keep the user's work as a separate custom preset instead.
                e = {**e, "name": display_stem(e["name"]) + "-custom"}
            entries.append({"name": e["name"], "description": e.get("description", ""),
                            "params": e["params"]})
        _user_cache = entries
    return [dict(e) for e in _user_cache]


def validate_custom_name(name: str):
    """Return an error message for an unusable custom preset name, or None if it's fine."""
    if not name:
        return "Please enter a name."
    if name.startswith(OFFICIAL_PREFIX):
        return 'Names starting with "*" are reserved for built-in presets.'
    bad = sorted({c for c in name if c in _ILLEGAL_NAME_CHARS})
    if bad:
        return "Names can't contain: " + " ".join(bad)
    if len(name) > _MAX_NAME_LEN:
        return f"Names can be at most {_MAX_NAME_LEN} characters."
    return None


def custom_preset_exists(name: str) -> bool:
    return any(e["name"] == name for e in load_user_presets())


def save_user_preset_from_config(name: str, description: str, config: dict) -> None:
    """Create or overwrite a custom preset, computing the params diff from defaults."""
    error = validate_custom_name(name)
    if error:
        raise ValueError(error)
    params = _params_to_save(config)
    presets = load_user_presets()
    for i, entry in enumerate(presets):
        if entry["name"] == name:
            presets[i] = {"name": name, "description": description, "params": params}
            break
    else:
        presets.append({"name": name, "description": description, "params": params})
    _write_user_presets(presets)


def delete_user_preset(name: str) -> None:
    _write_user_presets([e for e in load_user_presets() if e["name"] != name])


def _write_user_presets(presets: list) -> None:
    global _user_cache
    write_text_atomic(_user_presets_path(), json.dumps(presets, indent=2))
    _user_cache = None


# ---------------------------------------------------------------------------
# Search / browse
# ---------------------------------------------------------------------------

def _sort_key(e):
    # Sort on the name without the '*.' marker so a custom copy such as
    # 'Acid-Bubble-aqua-copy' lands right below '*.Acid-Bubble-aqua'.
    return display_stem(e["name"]).lower()


def search_presets(query: str = "", scope: str = "all") -> list:
    """Return preset entries matching query and scope, sorted by name.

    scope: 'all' | 'official' | 'custom'
    Each returned entry is a copy carrying a '_source' key: 'official' or 'custom'.
    """
    import presets

    results = []
    if scope in ("all", "official"):
        results += [{**e, "_source": "official"} for e in presets.PRESET_LIST]
    if scope in ("all", "custom"):
        results += [{**e, "_source": "custom"} for e in load_user_presets()]

    if query:
        q = query.lower()
        results = [e for e in results if q in e["name"].lower()]
    return sorted(results, key=_sort_key)


# ---------------------------------------------------------------------------
# Dev-only: write preset params back to the source .py file
# ---------------------------------------------------------------------------

# Category name → module filename stem (only exceptions to the lowercase rule)
_CATEGORY_FILENAME_MAP = {
    "break": "break_",
}


def _preset_name_to_module_stem(preset_name: str) -> str:
    """Map e.g. '*.Fire-Burn-terra' → 'fire', '*.Break-Stone-terra' → 'break_'."""
    category = display_stem(preset_name).split("-")[0].lower()
    return _CATEGORY_FILENAME_MAP.get(category, category)


def preset_source_path(preset_name: str):
    import pathlib
    stem = _preset_name_to_module_stem(preset_name)
    return pathlib.Path(__file__).resolve().parent.parent / "presets" / f"{stem}.py"


def _find_presets_list(tree):
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.List) and any(
                isinstance(t, ast.Name) and t.id == "PRESETS" for t in node.targets):
            return node.value
    return None


def save_official_preset_to_source(preset_name: str, config: dict) -> None:
    """Replace one entry's params in its presets/<type>.py file with the current config.

    Only that entry's lines are rewritten, so section comments, ordering and the
    formatting of every other preset are left exactly as they were. Param keys
    keep their existing order; new keys are appended. The edited file is
    re-parsed and checked before it is written. Dev-only (DEV_MODE).
    """
    import importlib
    import presets

    py_path = preset_source_path(preset_name)
    if not py_path.exists():
        raise FileNotFoundError(f"Preset source file not found: {py_path}")

    # newline="" keeps the file's own line endings (the preset files mix LF and CRLF),
    # so only the edited entry shows up in a diff.
    with open(py_path, encoding="utf-8", newline="") as f:
        src = f.read()
    eol = "\r\n" if "\r\n" in src else "\n"
    lines = src.splitlines(keepends=True)
    list_node = _find_presets_list(ast.parse(src))
    if list_node is None:
        raise ValueError(f"No 'PRESETS = [...]' list found in {py_path.name}")

    original = [ast.literal_eval(elt) for elt in list_node.elts]
    idx = next((i for i, e in enumerate(original) if e.get("name") == preset_name), None)
    if idx is None:
        raise ValueError(f"Preset '{preset_name}' not found in {py_path.name}")
    node = list_node.elts[idx]

    # The entry must occupy whole lines ("    {" … "    },") to be replaced cleanly.
    head = lines[node.lineno - 1][:node.col_offset]
    tail = lines[node.end_lineno - 1][node.end_col_offset:]
    if head.strip() or tail.strip() not in ("", ","):
        raise ValueError(f"'{preset_name}' shares a line with other code in {py_path.name}; "
                         "edit it by hand.")

    # Keys the entry already lists stay (even at their default value — authors write
    # e.g. GRAVITY_ANGLE: 180 on purpose), in their existing order; keys that newly
    # differ from the defaults are appended.
    new_params = _params_to_save(config)
    old_params = original[idx].get("params", {})
    ordered = {k: config[k] for k in old_params if k in config and k not in GUI_ONLY_KEYS}
    ordered.update({k: v for k, v in new_params.items() if k not in ordered})
    entry = {**original[idx], "params": ordered}

    new_src = ("".join(lines[:node.lineno - 1])
               + _format_entry(entry).replace("\n", eol)
               + "".join(lines[node.end_lineno:]))

    expected = original[:idx] + [entry] + original[idx + 1:]
    check = _find_presets_list(ast.parse(new_src))
    if check is None or [ast.literal_eval(e) for e in check.elts] != expected:
        raise ValueError(f"Edited {py_path.name} did not round-trip; nothing was written.")

    write_text_atomic(py_path, new_src, newline="")
    importlib.reload(importlib.import_module(f"presets.{py_path.stem}"))
    presets.rebuild()


def _format_value(v) -> str:
    """Format a single param value as Python source."""
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, str):
        return _dq(v)
    if isinstance(v, float):
        # Preserve up to 4 significant decimal places, strip trailing zeros
        s = f"{v:.4f}".rstrip("0").rstrip(".")
        # Ensure there's always a decimal point for floats
        if "." not in s:
            s += ".0"
        return s
    return repr(v)


def _dq(s) -> str:
    """Format a string or None value using double quotes, escaping as needed."""
    if s is None:
        return "None"
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _format_entry(entry: dict) -> str:
    """Serialize one preset dict in the presets/*.py house style (trailing newline included)."""
    lines = ["    {"]
    for key in ("name", "category", "locale", "intensity", "description"):
        lines.append(f'        "{key}": {_dq(entry.get(key, "" if key == "description" else None))},')
    extra = [k for k in entry if k not in ("name", "category", "locale", "intensity",
                                           "description", "params")]
    for key in extra:
        lines.append(f'        "{key}": {_format_value(entry[key])},')
    lines.append('        "params": {')
    for key, val in entry.get("params", {}).items():
        lines.append(f'            "{key}": {_format_value(val)},')
    lines.append("        },")
    lines.append("    },")
    return "\n".join(lines) + "\n"
