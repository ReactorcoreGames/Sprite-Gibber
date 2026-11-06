# Sprite Gibber — Guide

## Quickstart (TL;DR)

1. Unzip the download anywhere and double-click **`SpriteGibber.exe`**. No installer, no Python needed.
2. On the **Sprites & Export** tab, click **Add files…** or **Add folder…** and pick your sprite PNGs (pixel art on a transparent background; around 64x64px works best, but any size - even 512x512px - is possible but slower to process).
3. Go to the **Presets** tab and click a preset. The preview on the right plays the effect on your sprite right away.
4. Click **Export this sprite** (or **Export all**) under the preview. Your files land in a `gibbed` folder next to each sprite. Click **Open folder** to go there.

No sprites of your own yet? The **`example_sprites`** folder next to the exe has 35 animal sprites to try presets on. Add that folder in step 2. They're free to use, no attribution needed.

If the effect feels too confined, you can modify your sprites in your image editor to have wider margins, aka empty space around the object/character, to give the chunks/gibs more room to fly/move in.

That's all you need. The rest of this guide explains the other options.

---

## The window

- **Left side**: six tabs that control the effect: **Sprites & Export**, **Presets**, **Physics**, **Tint**, **Dissolve**, **Mask**.
- **Right side**: the **preview**, plus the export buttons underneath. It's always visible, whichever tab you're on.

Hover over almost any control to get a tooltip explaining what it does. Double-click a slider to reset it to its default.

## Your sprite list

The **Sprites & Export** tab holds the list of sprites you're working on. It's remembered between sessions, so you don't have to re-add them every time.

- **Add files…** / **Add folder…** add PNGs to the list. **Remove** takes the selected one out, **Clear** empties the list. None of these touch your actual files.
- Click a sprite in the list (or use **◀ Prev** / **Next ▶** above the preview) to show it in the preview.
- If a sprite has been moved or deleted since last time, it is dropped from the list when the app starts, with a short note.
- Large images (over 512×512) work but render slowly, and you'll see a warning. Gib effects are made for small pixel art, though not limited to them.

## Presets

The **Presets** tab lists all 479 built-in presets: 61 effect types (fire, cryo, electric, blood, meat, bone, acid, gold, crystal, glitch, matrix, nuclear, and many more), each in several variations.

- **Search**: type to filter, e.g. `fire`, `space` or `fire-burn`.
- **All / Official / Custom**: show everything, only the built-in presets, or only the ones you saved.
- Click a preset to load it. The preview updates and the description box tells you what the effect is going for.

### How preset names work

Names look like `*.Fire-Burn-terra-high`:

- `*` = a built-in preset (read-only). Your own presets have no `*`.
- `Fire` = the effect type, `Burn` = the variation.
- `terra` and the other locales describe the setting the effect happens in:
  - `terra`: normal ground and gravity, pieces fall and pile up on the floor.
  - `aqua`: underwater, pieces float upward or drift.
  - `depth`: crushing pressure, pieces get pulled into the middle.
  - `space`: zero gravity, pieces drift and spin freely.
  - `wave`: a sideways blast, pieces get thrown across the canvas.
  - `inner`: the effect bursts out from inside the sprite.
- An optional last part (`-high`, `-low`, `-fast`, `-heavy`…) marks a stronger, weaker or otherwise different version.

### Randomize

Also on the Presets tab, **Randomize** rolls new values for the setting groups you tick. Turn on **Vary current settings** to nudge the current look a little instead of starting from scratch. It's a quick way to discover variations of a preset.

## Tweaking: Physics, Tint, Dissolve, Mask

Every setting a preset uses is visible and editable on these tabs. Changing any of them marks the preset as modified (you'll see `-mod` in the export file names).

- **Physics**: how the sprite breaks and moves. Chunk count, blast mode (explode, implode, splits, shatter…), explosion force, gravity direction and strength, drag, spin and bounce. The **Seed** at the bottom rerolls the random break-up without changing the effect itself: same seed and settings always give exactly the same result.
- **Tint**: colour that bleeds into the pieces, such as burn marks, blood, frost, corrosion or glowing cracks. Turn it off with **Enable tint**.
- **Dissolve**: pixels fade away over the animation in a pattern, optionally shifting colour right before they vanish. Turn it off with **Enable dissolve**.
- **Mask**: a shape (circle, star, gears, cross…) that cuts the animation into a silhouette as it plays.

Advanced options sit in collapsed sections (for example **More motion options**). Any that a preset uses open automatically and show "N in use", so nothing is hidden from you.

## Live preview

- With **Live** switched on (next to **Update Preview**), the preview re-renders a moment after you stop changing settings. With it off, click **Update Preview** yourself.
- If a render takes too long (big sprite, huge chunk count), live mode pauses itself and says so. Click **Turn live preview back on** when you're ready.
- **Play Loop** / **Stop**, the scrubber and the **◀ ▶** buttons let you inspect single frames. **Zoom** sets the magnification.
- The small swatches beside the preview (**LUMI**, **COLR**, **SATU**, **CHEC**) change the preview background so you can check your effect against light, dark or coloured backdrops. They don't affect exported files, unless you tick *Use preview background colour in GIF*.
- **Frames** sets how many frames the animation has (default 16). This is your setting and stays the same when you switch presets.
- Preview playback uses the same timing as the exported GIF.

## Exporting

The buttons under the preview:

- **Export this sprite**: just the sprite currently in the preview.
- **Export all (N)**: every sprite in your list, with the current settings.
- **Stop** cancels a running export. **Open folder** opens the export folder.

### Where files go (Export To, on Sprites & Export)

- **Next to each sprite, in a gibbed/ subfolder** (default): `MyGame/sprites/lion.png` exports to `MyGame/sprites/gibbed/`.
- **This folder**: everything goes into one folder you choose with **Choose folder…**.

Each export gets its own subfolder named `<sprite>_<effect>`, for example `lion_Fire-Burn-terra`, `lion_Fire-Burn-terra-mod` (you tweaked it) or `lion_MyCoolPreset`. Exporting the same sprite with the same effect again replaces the earlier result, so stale frames never pile up.

### What you get (Output Files, on Sprites & Export)

Tick any combination:

- **Frame PNGs**: `lion_Fire-Burn-terra_00.png`, `_01.png`… Frame 00 is the intact sprite; the last frame is the settled or faded end state. Same canvas size as your sprite, transparent background.
- **Spritesheet**: all frames in one PNG (`_sheet.png`). **Frames per row** sets the layout (0 = one long row).
- **Animated GIF**: for previews, devlogs and sharing. **GIF Scale** upscales it with crisp pixels (4× by default). **GIF Frame speed** sets the ms per frame, and **Pause first frame** / **last** set how long the start and end frames hold. GIFs only support on/off transparency, so very faint pixels drop out. Use the PNGs in your game.

Settings are captured when an export starts, so changing presets mid-export won't mix effects.

## Your own presets

Found a look you like? On the Presets tab under **Preset Actions**:

- **Save As Copy…**: save the current settings as a new custom preset with your own name. Works whether you started from a built-in preset, a custom one, or from scratch.
- **Save Changes**: overwrite the loaded custom preset with your tweaks. Built-in presets can't be overwritten; use Save As Copy instead.
- **Revert**: throw away your tweaks and reload the preset as saved.
- **Delete**: remove a custom preset, after a confirmation.

Custom presets show up in the list without the `*` and are kept in `user_presets.json`.

## Where your settings and logs live

Everything is stored in the same folder as `SpriteGibber.exe`. Nothing goes into AppData or the registry.

- `config.json`: your last settings, sprite list, export choices and window layout.
- `user_presets.json`: your custom presets. **Back this up** (or copy it into a new version's folder) to keep your presets.
- `sprite_gibber.log`: error log. If something goes wrong, the error dialog has an **Open Log** button; include this file in bug reports.
- `assets/masks/`: the black-and-white PNG shapes used by the Mask tab. You can add your own: white = visible, black = cut away. Click **Refresh** on the Mask tab to pick them up.

To start fresh, close the app and move `config.json` somewhere else. A new one is created on the next start. If a settings file ever gets corrupted, the app sets it aside (renamed `*.corrupt-1.json`) instead of wiping it.

Because files are written next to the exe, put the folder somewhere you can write to, such as Documents or Desktop, rather than `C:\Program Files`.

## Tips

- **Tune on one sprite, then Export all.** Settings apply to every sprite in the list.
- **Flip through sprites with Prev/Next** while a preset is loaded, to see how one look reads on different shapes.
- **Small canvases are tight.** A sprite that fills its whole 32×32 canvas has no room for pieces to fly, so they pile against the walls. A little transparent padding around the sprite gives effects more room.
- **Gravity direction** (Physics tab): 0° = up, 90° = right, 180° = down, 270° = left. Pieces settle against the wall(s) gravity points at.
- **Fewer chunks = chunkier, more readable pieces**. Many chunks = dust and spray.

## Contact & links

Questions, bugs, or showing off what you made: reactorcoregames@gmail.com

Check out everything else I do: ✨🚀

- Home/Links: https://linktr.ee/reactorcore
- Releases: https://reactorcore.itch.io
- Blog: https://www.patreon.com/ReactorcoreGames
- Discord: https://discord.gg/UdRavGhj47
- Catalog: https://reactorcoregames.github.io/

-Reactorcore
