from . import (
    fire, cryo, electric, plasma, water, acid, singularity, blade, hammer,
    slash, grenade, bullet, void, psychic, arcane, holy, heal, photon, flash,
    shadow, blood, meat, bone, biodegrade, rot, plague, wither, stone,
    gold, crystal, rust, goo, sand, break_, crush, grind, shred, laser,
    ion, crack, disintegrate, evaporate, liquify, smoke, ash, entropy,
    glitch, chromatic, matrix, tar, fungal, spore, brimstone, curse,
    vanish, burst, clamp, squeeze, flatten, nuclear, antimatter,
)

_MODULES = (
    fire, cryo, electric, plasma, water, acid, singularity, blade, hammer,
    slash, grenade, bullet, void, psychic, arcane, holy, heal, photon, flash,
    shadow, blood, meat, bone, biodegrade, rot, plague, wither, stone,
    gold, crystal, rust, goo, sand, break_, crush, grind, shred, laser,
    ion, crack, disintegrate, evaporate, liquify, smoke, ash, entropy,
    glitch, chromatic, matrix, tar, fungal, spore, brimstone, curse,
    vanish, burst, clamp, squeeze, flatten, nuclear, antimatter,
)


def rebuild():
    """(Re)build the registry from the type modules — called again after a module
    is reloaded (dev "Save to Source"), so PRESETS/PRESET_LIST reflect the edit.
    Callers must look these up via the package (`presets.PRESETS`) at use time."""
    global PRESETS, PRESET_LIST
    all_presets = [p for m in _MODULES for p in m.PRESETS]
    # dict keyed by name for O(1) lookup (used by params.py and app.load_preset)
    PRESETS = {p["name"]: p for p in all_presets}
    # flat list for the GUI browser (search/filter)
    PRESET_LIST = all_presets


rebuild()
