# Sprite Gibber — Mask Catalog

Shape reference for `FRAME_MASK`, built from a contact-sheet pass over all 107 files in
`assets/masks/`. Read this before reaching for a mask in a preset brief.

**Filenames are for the user's browser, not for you.** Don't assign a mask by its name
matching a Main Type's name (e.g. don't reach for `Y Gears` just because a preset is
"mechanical," or `E Moon` just because a preset is "lunar"). Judge every mask by its
actual silhouette and how that silhouette interacts with the sprite and the physics —
the name is a mnemonic for the user's dropdown, nothing more.

Remember every mask can be `FRAME_MASK_FLIP`ped, `FRAME_MASK_MIRROR`ed, and
`FRAME_MASK_ROTATE90`'d — a "moon" pointing left is the same file as one pointing up.
Direction/orientation is never a reason to rule a mask out.

---

## The two legitimate reasons to reach for a mask

Masks are destructive — they erase pixels outright, fast, wherever the mask is black.
Only use one when it's clearly one of these two cases, not as decoration:

1. **The mask's shape *is* the preset's gimmick.** The animation is meant to read as
   "this sprite is being erased/framed/revealed in the shape of X" — the mask silhouette
   is the point, not a side effect. Worth naming explicitly in the preset brief.
2. **Containment aid for an otherwise risky/extreme preset.** Some presets (violent
   `EXPLODE`, `noise`/`repulsor`/`orbital` gravity modes, small canvases, high `SPREAD`)
   produce chunks or stray pixels that hug or cross the canvas edge in a jarring way. A
   soft vignette-style mask (see Group A/G below) cleans that up without being "about"
   any shape at all — it should be nearly invisible as a design choice, just a fix.

If neither reason applies, don't add `FRAME_MASK`. A mask bolted on for novelty just
looks like part of the sprite is randomly missing.

---

## Group A — Rounded (soft vignette family)

`A Rounded (1)`–`(4)`: square → increasingly rounded corners → full circle/oval. No
border line, just a soft-edged crop. Pure containment-aid shapes — use when a preset's
physics send pixels too close to the corners and you want a gentle round-off rather than
a hard frame. Pick the roundness level ((1) barely rounds corners, (4) is a full circle)
by how aggressively the preset's chunks approach the corners.
Typically 'A Rounded (2)' is most commonly used for typical 'space' locale + chunk explosion based presets to safeguard from the result of having pixels congregate at the corners of animation, even if some pixels will continue to linger near the edges due to chunks going off-screen.

## Group G — Frame (bordered vignette / edge-cleanup family)

`G Frame (0)`: a plain 4px-thick rectangular border erasure — crops a thin strip off
all four edges. Purpose-built containment aid: use this whenever a preset's chunks or
loose pixels visibly slide along or hug the canvas edge in a way that reads as a bug
rather than a physical result (common with tight canvases + strong `EXPLODE`, or
`noise`/`repulsor` gravity that pushes stray pixels to the wall). This is the "default
fix" mask — reach for it first when a preset needs edge cleanup and no particular shape
is called for.

`G Frame (1)`–`(3)`: the same edge-cleanup idea as `(0)`, but smoothed/rounded and with
the border rendered as a thin 2px black outline rather than a flat crop — same
containment purpose as Group A's roundness progression, but with the added edge-defining
line. Visually near-identical to `A Rounded (1)`–`(3)` at a glance; choose `G` over `A`
when the preset benefits from that thin defining outline (gives the vignette a slightly
more "framed/vignetted" look rather than a soft fade), choose `A` when you want the
edge-fade with no border line at all.

## Group B — Ovals / Shaft

Two ovals (upright, wide) and three vertical bar/slab shapes (full-height slab, two
narrower slabs). These read as beams, columns, or a single elongated silhouette slicing
through the sprite. Good as a shape-gimmick when the preset's story is "reduced to a
single vertical/oval remnant" (e.g. an implode/depth preset that should visually collapse
down to one narrow surviving strip) rather than as a themed prop.

## Group C — Shape (regular polygons)

`(1)` triangle, `(2)` pentagon, `(3)` hexagon, `(4)`–`(5)` heptagons, `(6)` octagon,
`(7)`–`(8)` near-circular polygons. A clean geometric-solid family. Shape-gimmick use:
any preset where the *remaining silhouette itself* should read as a deliberate geometric
solid rather than the original sprite outline — e.g. "petrifies/crystallizes into a
perfect polygon" as the punchline of the animation. Not a default containment choice
(polygons are much more visually assertive than Group A/G) — only reach for these when
the polygon shape is explicitly part of the brief.

## Group D — Cross

Three plus/cross shapes, thin to thick arm width. A strong graphic silhouette — use only
when a cross-shaped remainder or reveal is the explicit visual beat of the preset (a
called-out shape gimmick), never as a generic "this is a holy-ish preset" default. The
arm thickness is the only real variable: thinner reads more like a precise cut, thicker
reads more like a blunt stencil.

## Group E — Moon (crescents / directional arcs)

Three crescent shapes at different thicknesses. Despite the name, think of these as
**directional wave/pulse arcs**, not literal moons — a crescent is a curved edge with a
clear "open" and "closed" side, and with flip/mirror/rotate it can point any of four
ways. Good shape-gimmick fit for anything that should read as a directional pulse,
shockwave-front, or a bite/scoop taken out of the sprite from one side — pick thickness
by how much of the sprite the "bite" should consume.

## Group F — Diamond

`(1)` clean diamond (rotated square), `(2)` a jagged/scalloped diamond (rough edge,
crack-adjacent silhouette), `(3)` a narrow/tall diamond. `(2)`'s raggedness makes it the
most interesting of the three as a genuine shape-gimmick (a shattered-crystal-shaped
remainder); `(1)` and `(3)` are cleaner and read more like a stencil cut than damage.

## Group X-Bang — jagged bursts

Eight spiky, irregular star/burst outlines (comic "impact" shapes, asymmetric spike
counts). Strong shape-gimmick candidate for anything where the *reveal/erase shape*
should itself look like an explosion or impact silhouette — e.g. a preset whose last
frame should read as "blown apart in the shape of a shockwave," not just physically
scattered. Too visually loud to use as a quiet containment aid.

## Group X-Splat — organic blobs (37 variants, largest group)

Irregular blob/splatter outlines, varying arm count and raggedness from tight/round to
wildly spiky. This is the one group whose *shape family* (organic, asymmetric, wet-
looking silhouette) is close enough to certain material identities that it can
legitimately double as a strong shape-gimmick for a preset whose entire animation is "the
sprite's final form is an irregular splat" — but that's still a shape judgment made per
preset (does *this* preset's story end in a splat shape?), not an automatic pick for an
entire Main Type just because the type sounds organic/liquid. Pick the raggedness level
to match how violent the preset's ending should look: tighter/rounder variants for a
contained puddle-like remainder, spikier variants for a violent splatter silhouette.

## Group Y-Flower — petal shapes

Five petal arrangements (4 to 8 petals, one rounded-diamond hybrid). Shape-gimmick use
only when the brief explicitly wants a radiating/petal-like final silhouette — a bloom,
a radiating burst pattern read as petals rather than a starburst. Petal count changes the
density of the radiating pattern, not the "meaning."

## Group Y-Gears — cog / mechanical outlines

Nine variants: solid gear, thin-spoke gear, open-center gears at various tooth counts, a
hex-nut, a spiky sun-gear, a spoked wheel. **Don't reach for these just because a preset
is mechanical** — that's the exact name-matching trap to avoid. The legitimate
shape-gimmick case is narrower and more interesting: the toothed/notched silhouette and
open center are useful whenever a preset's story benefits from a *radially symmetric,
partially-hollow reveal shape* — which is just as valid for an arcane/ritual preset
(a rune-circle-like remainder) as for anything mechanical. Judge by "does a toothed ring
silhouette serve this preset," not by the filename.

## Group Y-Starss — stars

Three star shapes (clean 5-point, asymmetric 5-point, nautical/pointed star). Same rule
as Y-Flower: reach for these when a radiating star silhouette is the explicit visual
punchline, not as a default for "celestial-sounding" types.

## Group Z-Arrow — directional shapes

Fifteen variants: double-headed arrow, single arrows (several head styles), chevrons,
curved/rotate arrows, a U-turn arrow, a stacked-chevron "wings" pair, a 4-way d-pad
cross, a single curved corner-turn. The one group where the shape is inherently about
*direction* rather than containment or texture — legitimate shape-gimmick use is a
preset whose reveal/erase should visually point along the blast/gravity vector (most
naturally a `wave`-locale preset, but judge each preset on whether a directional arrow
silhouette actually adds to its specific story, not merely because it has lateral
gravity).

---

## Quick decision rule

Before setting `FRAME_MASK` in any preset:

1. Is this preset's ending *about* a specific shape? → pick from C/D/E/F/X-Bang/X-Splat/
   Y-Flower/Y-Gears/Y-Starss/Z-Arrow based on the actual silhouette, and say so in the
   preset's description.
2. Is this preset otherwise fine but has jarring edge-hugging pixels/chunks? → `G Frame
   (0)` first, or an `A Rounded`/`G Frame (1–3)` vignette if a softer fade reads better.
3. Neither? → don't set `FRAME_MASK`.
