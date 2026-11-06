# Meat — 10 presets (registry #201–210)

Module: `presets/meat.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Classic bloody meat gibs in sizes small / medium / large / XL, plus a single skinned dead-weight mass.

**Gimmick lock** (new): **Gibs that stay**: no dissolve (except `Gib-aqua`'s dispersal), wound tint on the chunk borders (`TINT_MODE="chunks"`), and the size ladder small → medium → large → XL → single is the type's spine.

**Locales present:** terra ×5, aqua, depth, space, wave, inner.

**Why these locales:** terra carries the size ladder; aqua, depth, space, wave, inner one each.

**Current state (2026-10-30):** chunks 1–90, explode 0.2–3.4; blast: explode 7, implode 1, horizontal_split 1, burst 1; gravity: directional 9, centripetal 1; tint on 10/10, dissolve 1/10, mask 1/10, stretched chunks 0/10.

**Stage 3 notes:**

- Compare with `*.Blood-Gibs-terra`: Meat is chunkier and crimson; the classic Blood gib is the plain reference.

## Stage 3 result (2026-10-31, session 3a)

- **Style change (user):** materials are now *textured and believable*, not flat garish fills. Meat is a mottled two-tone: a dark muscle-crimson front (`#6A0814`, depth ≈ one chunk radius, `TINT_JITTER_OUTER` 1.0, `TINT_NOISE` 0.5) blended into raw red (`#D8202C`), `TINT_SATURATION_SHIFT` +0.1, and `TINT_GRAIN` 0.18 (new parameter, added this session for exactly this). Small-piece presets (`-small`, `Pulp-depth`, `Spray-wave`) use the inverse — deep raw-red body front plus jittered dark specks from the core, `TINT_BLEND` 0.08, grain 0.25 — because 1–2 px pieces are all border and a border front paints them one flat colour.
- Lock kept. Every preset is bidirectional chunks mode with `blend` collision; `outer_wins` was dropped because the jittered low-opacity tail of a thin rim front wins over the full body and lets the pale bear show through.
- `Skinned-terra-single` is a `burst` toss of the single chunk; on the confined bear it can't move (boxed-in-bear limit, flag expected), on the lion it hops and lands as dead weight. `Drift-space` uses `burst` (an explode from the canvas centre pushed the bottom-sitting lion into the floor) and stretched steak slabs; `Spray-wave` is a low-force shatter carried right by 90° gravity with horizontal streaks; `Gib-aqua` frays each piece from its edge (`centrifugal`) into dark blood.

- **Final pass (2026-10-31):** `Pulp-depth` clumped by frame 3–5 of 15 and then sat as a static lump for the rest of the GIF (no dissolve to carry it). Centripetal slowed to strength 0.3 / drag 0.32 (drag-limited creep), so the pieces converge over the whole animation. Sheet: `shots/stage3-final/depthfix/`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

201. `*.Meat-Gib-terra-small` — classic gibbing, many small chunks; high CHUNKS, high EXPLODE, high SPIN, crimson bidirectional tint at moderate TINT_OPACITY, no dissolve so all the meaty fragments remain visible
202. `*.Meat-Gib-terra-medium` — classic gibbing, medium chunk count; moderate CHUNKS, moderate EXPLODE and SPIN, crimson tint, no dissolve
203. `*.Meat-Gib-terra-large` — fewer, larger meat chunks; low CHUNKS, moderate EXPLODE, crimson tint with TINT_DEPTH_OUTER larger so each big chunk shows more wound color, no dissolve
204. `*.Meat-Gib-terra-xl` — a handful of huge meat chunks; very low CHUNKS, lower EXPLODE so the heavy pieces don't fly far, crimson tint, no dissolve
205. `*.Meat-Skinned-terra-single` — body collapses as one skinned dead-weight mass; SINGLE_CHUNK=True, low EXPLODE so it barely moves before settling, crimson tint at high TINT_OPACITY_OUTER for an exposed-flesh look, no dissolve
   - **Flag:** confined: sim ended after 1 tick(s); wide: sim ended after 1 tick(s)
206. `*.Meat-Gib-aqua` — gibbed underwater, chunks drift upward as they tumble; GRAVITY_ANGLE=0 chunks rise, moderate CHUNKS, crimson tint, slow dissolve (DISSOLVE_CURVE>1) as the meat disperses while floating up
207. `*.Meat-Pulp-depth` — body crushed inward into a mass of pulped meat; BLAST_MODE=implode, high CHUNKS, crimson tint with TINT_COLLISION=inner_wins, no dissolve so the pulped mass remains
   - **Flag:** wide: only 14/16 distinct frames
208. `*.Meat-Drift-space` — zero-gravity gibbing, chunks tumble outward in all directions; GRAVITY_STRENGTH=0, moderate CHUNKS, moderate EXPLODE, crimson tint, no dissolve
209. `*.Meat-Spray-wave` — struck laterally, meat chunks fly off in the hit direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, high CHUNKS, crimson tint at high TINT_OPACITY_OUTER, no dissolve
210. `*.Meat-Rupture-inner` — internal rupture bursts the body apart from its core; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER deep-crimson core, high CHUNKS, no dissolve
