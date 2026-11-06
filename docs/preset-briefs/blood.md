# Blood — 8 presets (registry #193–200)

Module: `presets/blood.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Liquify into a blood pool, burst into a mist, spray. Ketchup red. Also home of the restored original preset that started the project.

**Gimmick lock** (new; revised in Stage 3): **Liquid gore droplets**: very high chunk counts (150+), opaque ketchup red (opacity 1.0, no bleed except `Mist`/`Cloud`), `TINT_ANIM="instant"` (an `early` ramp makes the first frames pink) with crimson darkening arcs. The restored `*.Blood-Gibs-terra` is the deliberate exception — the classic 16-chunk gib, keeping the original's mechanics (its tint was made juicier in the 2026-10-31 tweak pass).

**Locales present:** terra ×3, aqua, depth, space, wave, inner.

**Why these locales:** All six; terra has pool / mist / heavy splatter.

**Current state (2026-10-30):** chunks 160–280, explode 0.22–3.0; blast: explode 7, horizontal_split 1; gravity: directional 7, centripetal 1; tint on 8/8, dissolve 8/8, mask 1/8, stretched chunks 0/8.

## The original Blood preset (restore as-is in Stage 3)

**Restored 2026-10-30 (Stage 3 session 1):** first entry of `presets/blood.py` with exactly the params below; smoke test passes. Leave it untouched in session 2.

**Source:** `blood_gibs`, the first entry of the original `presets.py` and the default `PRESET` in the original `params.py` (June 2026 snapshot at `C:\ClaudeWorkspace\Sprite Gibber - Copy\`). It is the project's founding effect: the wound-bleeding gib from the blog post in `docs/Sprite-Gibber-idea.md`. The current defaults `TINT_COLOR_OUTER="#660000"` / `TINT_COLOR_INNER="#FF2222"` are inherited from it.

**Original bundle (old engine):**

```python
"blood_gibs": {
    "TINT_DEPTH": 4, "TINT_COLOR_OUTER": "#660000", "TINT_COLOR_INNER": "#FF2222",
    "TINT_OPACITY": 0.9, "TINT_ALPHA_BLEED": 0.2, "TINT_MODE": "chunks",
    "TINT_ANIM": "linear",
    "BLAST_MODE": "explode", "EXPLODE": 3.0, "GRAVITY_ANGLE": 180,
    "GRAVITY_STRENGTH": 1.5, "DISSOLVE": False,
}
# inherited from the old params.py: CHUNKS 16, DRAG 0.18, SPREAD 1.2, SPIN 8.0, EDGE_ZONE 6, SEED 42, FRAMES 8
```

**Translation to the current engine:** the old tint was exactly today's unidirectional tint without jitter: dark `#660000` at the chunk border, ramping to bright `#FF2222` at the cutoff, opacity falling from 0.9 to 0 over the depth. The only scale change is depth: old `TINT_DEPTH` was 4 pixels, today's is a fraction of √(opaque pixels). `0.18` gives 4 px on a typical ~400-pixel 32×32 sprite (3–5 px across the animal set; 5 px on `confined_32`, 4 px on `wide_64`). Jitter must be `0.0` because the old engine had none. The other values equal today's defaults but are written out, so later default changes can't drift the preset.

```python
{
    "name": "*.Blood-Gibs-terra",
    "category": "Blood",
    "locale": "terra",
    "intensity": None,
    "description": "The original Sprite Gibber effect: classic bloody gibs. Sixteen chunks blast outward and fall, each with a dark-to-bright red wound along its broken edges.",
    "params": {
        "CHUNKS": 16,
        "BLAST_MODE": "explode",
        "EXPLODE": 3.0,
        "GRAVITY_MODE": "directional",
        "GRAVITY_ANGLE": 180,
        "GRAVITY_STRENGTH": 1.5,
        "DRAG": 0.18,
        "SPREAD": 1.2,
        "SPIN": 8.0,
        "EDGE_ZONE": 6,
        "TINT_BLEND_MODE": "unidirectional",
        "TINT_MODE": "chunks",
        "TINT_COLOR_OUTER": "#660000",
        "TINT_COLOR_INNER": "#FF2222",
        "TINT_DEPTH_OUTER": 0.18,
        "TINT_OPACITY_OUTER": 0.9,
        "TINT_JITTER_OUTER": 0.0,
        "TINT_ALPHA_BLEED_OUTER": 0.2,
        "TINT_ANIM": "linear",
        "DISSOLVE": False,
    },
},
```

- **Name:** `*.Blood-Gibs-terra` (from `blood_gibs`; rename freely, it's new). Put it **first** in `presets/blood.py` so it heads the Blood group. That makes the library 479 presets.
- **Verified in Stage 2:** the old engine was run on both test sprites and compared with this translation at 8 and 16 frames — `shots/blood-original/blood_gibs_old_vs_new.png`. Wound colour, depth and the final dark-red pile match. Remaining differences come from engine fixes, not params: frames are now spread evenly over the whole simulation (the first frames show less separation), floors are the canvas edge (the old floor was the sprite's lowest pixel — identical for sprites that touch the canvas bottom), and landed pieces skid with floor friction instead of freezing.
- **Leave alone:** no dissolve, no extra keys, no "improvements". `FRAMES` was 8 in the old CLI but is user-controlled now (default 16) and must not go in `params`. The old GIF timing (80 ms per frame) equals today's `MS_PER_FRAME` default; the old holds were global CLI settings, not part of the preset, so leave the hold keys out.
- **Ancestor, for reference only:** the blog post's example values (`chunks 48, explode 3, gravity 1.4, drag 0.22, spread 1.15, spin 9, woundDepth 2, frames 20`) are where `blood_gibs` came from. Not the preset to restore.

## Stage 3 result (2026-10-31)

- **Lock revised:** `TINT_ANIM="instant"` (not `early`): the `early` ramp is what made frame 1 pink. All presets are flat opaque ketchup red (`#E8000E`–`#FF1A1A`, edges mode, `TINT_SINGLE_COLOR`, depth 3.0, `TINT_SATURATION_SHIFT` +0.3), darkening via crimson arcs (`#A0000E` → `#600006`) and dark-clot fade colours (`#5A0004`). `Cloud-aqua` is the translucent exception (bleed 0.4, noisy edges).
- Dark-hearted droplets (bidirectional, 1 px dark core, `inner_wins`) don't work at 160+ chunks: the 1 px inner front already spans each droplet, so `inner_wins` suppresses the red body and the sprite shows through. Dropped in favour of the colour arcs.
- `*.Blood-Gibs-terra` was left untouched in the overhaul itself (byte-identical entry).

## Tweak pass (2026-10-31, user review)

- **`*.Blood-Gibs-terra` — juicier wound.** The original read as desaturated and muddy: in unidirectional tint, opacity falls `1 − t` while the colour shifts toward the inner colour, so the bright inner red never really shows — only the dark edge, the sprite's own colours, and 0.2 alpha bleed. Now outer `#8A0008` (was `#660000`), inner `#FF1A1A` (was `#FF2222`), `TINT_DEPTH_OUTER` 0.3 (was 0.18), opacity 1.0 (was 0.9), alpha bleed 0.05 (was 0.2), `TINT_SATURATION_SHIFT` +0.4 (new). Physics, chunking and the `linear` ramp stay original, so it still starts as pale chunks that redden as they fall; the final pile is saturated deep red instead of brownish pink. It no longer matches the Stage 2 old-vs-new comparison above; that's intentional.
- **`*.Blood-Mist-terra-fine` — darker secondary speckle.** It read as too single-coloured. Texture comes from the dissolve fade: `DISSOLVE_FADE_COLOR` `#6A000A` (was `#B00010`), strength 1.0 (was 0.9), `DISSOLVE_CHUNK_STAGGER` 0.6 (was 0.3), so droplets darken one by one before they drop out — a mild dark-red speckle from frame 2 onward. Tried and rejected: chunks-mode bidirectional dark cores (barely visible at 1–3 px droplets, white leaks through) and edges-mode noise/jitter on a second colour (opacity falls with depth, sprite pixels show through).
- Variant sheets: `shots/blood-tweak/` (v1–v3 plus the final `Blood-_01.png`).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

193. `*.Blood-Pool-terra` — body liquifies into a pool of blood; high CHUNKS, low SPIN, moderate EXPLODE, ketchup-red bidirectional tint at max TINT_OPACITY, BOUNCE=0 so chunks settle dead-stop into a flat pile, no dissolve so the pool stays visible
194. `*.Blood-Mist-terra-fine` — fine blood mist cloud; very high CHUNKS, high EXPLODE and SPREAD so droplets scatter widely, ketchup-red tint, fast dissolve (DISSOLVE_CURVE<1) as the mist disperses and fades
195. `*.Blood-Splatter-terra-heavy` — heavy violent splatter; very high CHUNKS, extreme EXPLODE, ketchup-red tint at high TINT_OPACITY_OUTER, moderate dissolve as droplets settle and the finer mist fades out
196. `*.Blood-Cloud-aqua` — blood billows upward into water like ink; GRAVITY_ANGLE=0 chunks rise, high CHUNKS, low SPIN, ketchup-red bidirectional tint with high TINT_ALPHA_BLEED_OUTER for a diffusing cloud edge, slow dissolve (DISSOLVE_CURVE>1) as it disperses while rising
197. `*.Blood-Collapse-depth` — body collapses inward into a clot of blood; BLAST_MODE=implode, high CHUNKS, ketchup-red tint with TINT_COLLISION=inner_wins, moderate dissolve as the mass thickens and shrinks
198. `*.Blood-Drift-space` — zero-gravity blood droplets scatter and float; GRAVITY_STRENGTH=0, high CHUNKS, moderate EXPLODE so droplets drift outward, ketchup-red tint, slow dissolve (DISSOLVE_CURVE>1) as droplets fade over many frames
199. `*.Blood-Spray-wave` — struck laterally, blood sprays in the hit direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, very high CHUNKS, ketchup-red tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing droplets fade last
200. `*.Blood-Rupture-inner` — internal rupture, blood bursts outward from the core; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER deep-red core spreading to a brighter outer edge, high CHUNKS, DISSOLVE_PATTERN=centrifugal as the spray disperses outward from center
