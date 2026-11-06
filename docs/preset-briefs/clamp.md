# Clamp — 4 presets (registry #453–456)

Module: `presets/clamp.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** An external vice splits the body cleanly in two.

**Gimmick lock** (kept): always a split `BLAST_MODE`, low-moderate chunks for two chunky halves, no tint, no dissolve.

**Locales present:** terra ×2, depth, space.

**Why these locales:** terra, depth, space.

**Current state (2026-10-30):** chunks 6–10, explode 0.4–1.6; blast: vertical_split 3, implode 1; gravity: directional 3, centripetal 1; tint on 4/4 (4 only via the default), dissolve 0/4, mask 0/4, stretched chunks 0/4.

**Stage 3 notes:**

- **Tint is currently on** (default red wound tint) — set `TINT_DEPTH_OUTER=0`.
- Apply the split-axis convention from Blade/Slash: `vertical_split` pairs with `halves-h`.

## Stage 3 result (2026-10-31, session 5b)

- Lock kept and tightened: a split `BLAST_MODE` on every preset, now always `horizontal_split` + `CHUNK_BIAS="halves-v"` (left/right halves), `TINT_DEPTH_OUTER=0` (inherited red wound tint gone), `DISSOLVE=False`. Split modes cut at the **canvas** centre, so `vertical_split` can't cut the bottom-anchored lion top/bottom (every chunk is below the centre row and just falls). The brief's `vertical_split` lines were replaced for that reason.
- Kept apart from Blade (2 chunks, stretch 3, a crimson wound line): Clamp halves are round, blocky and cracked (2–10 chunks, no stretch, no tint), heavy, with a thud bounce.
- Variety: 8 blocks that lurch apart, topple and thud down with `BOUNCE` 0.2 (`Vice-terra`); one clean crack whose two halves only slip apart and sag (`-tight`, 2 chunks, drag 0.25); `Crush-depth` stays a split (the brief's `implode` broke the lock) with centripetal gravity after a 4-tick ramp, so the halves spring apart and are dragged back into one crumpled wreck; halves float apart turning slowly in zero gravity (`Drift-space`).
- On the boxed-in bear the halves start against the side walls, so the split reads mostly as toppling (the same engine limit as Blade).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

453. `*.Clamp-Vice-terra` — clamped and split cleanly in two, halves fall apart under gravity; BLAST_MODE=vertical_split, moderate EXPLODE, no tint, no dissolve so the split halves remain
454. `*.Clamp-Vice-terra-tight` — tighter clamp, less initial scatter before halves settle; BLAST_MODE=vertical_split, low EXPLODE, no dissolve
455. `*.Clamp-Crush-depth` — the vice doesn't release, it keeps crushing inward past the split into a compact wreck; BLAST_MODE=implode, GRAVITY_MODE=centripetal, no dissolve so the crushed mass remains
456. `*.Clamp-Drift-space` — zero-gravity clamp release, split halves drift apart and hang with no settle; BLAST_MODE=vertical_split, GRAVITY_STRENGTH=0, no dissolve
