# Sprite Gibber — Promo notes (internal, not shipped in the release zip)

## Strategy

### What this is, in one line

A standalone Windows tool that turns any pixel art sprite into a ready-to-use death/destruction animation (frame PNGs, spritesheet, GIF), with 479 presets so a non-animator gets a good result in one click.

### Who it's for

- Solo and hobby indie devs who need death/hit/destroy animations for lots of enemies, props and crates, and can't hand-animate each one.
- Game jam participants: drop in 20 sprites, Export all, done.
- Pixel artists who want a quick "explode it" effect for a portfolio or devlog GIF.

### Why it gets found

The output is the advertisement. A grid of animals bursting into fire, ice, gold, slime and glitch is instantly understandable and very shareable, so lead with the GIFs everywhere (`promo/showcase_grid_3x.gif` — one animal per effect type, all 61 — and the per-effect 4× GIFs in `showcase_gifs/`, kept out of the release zip but ready for devlogs and social posts). Text comes second.

### Tactics

- **Post in persistent, searchable places first** (itch.io page, GitHub repo, Lospec software page, curated tool lists, AlternativeTo). These keep sending traffic for years without upkeep, unlike one-off social posts.
- **Pin a GIF as the first gallery item** on itch.io and as the first image in the GitHub README. People decide in about a second.
- **Name the effect types in text** (fire, ice, blood, acid, gold, glitch, nuclear…). Searchers type "pixel art explosion" or "death animation generator", not "gibbing".
- **Give away example output.** A free CC0 pack of gibbed sprite sheets on OpenGameArt/itch, with "made with Sprite Gibber" and a link, puts the tool in front of people browsing for assets, who are exactly the audience.
- **Devlog drip:** one GIF per effect type is 61 ready-made posts for itch devlogs, Bluesky/Mastodon/X `#pixelart` `#gamedev` `#indiedev`, and the Discord.
- **Short video:** a 30–60 s silent-ish showcase cut from the GIFs works as a YouTube upload and a Short. There's no voiceover to maintain, so it never goes stale.

### Business model: honest estimate

- **Market reality:** sprite/VFX helper tools on itch.io are a small niche. The ones that earn real money are either broad editors (Aseprite, Pixel Composer) or very polished single-purpose tools with a long track record. A first release of a niche Windows-only tool will mostly earn **attention**, not revenue.
- **The plan (your call): paid Windows build on itch.io + MIT source on GitHub.** This is a sound model for a tool like this. Laypeople pay for the convenience of a ready, double-click build. Devs who want to tweak it, and employers judging your work, get the code. Open source also makes the tool eligible for the "awesome" lists and GitHub topic pages, the best long-term traffic sources here, and every one of those listings points back to the paid build.
- **What to expect:** the GitHub side brings reach and portfolio value. The itch side converts a slice of that into sales. Under MIT anyone *may* build and share the exe themselves; very few laypeople will, and a clear "buy the ready build to support development" line in the README and on itch covers it.
- **Levers that fit this model:** a launch discount for early buyers, itch bundles and sales events, a demo GIF-heavy page, and putting the itch link at the very top of the GitHub README. Raise the price later as ratings and comments build up, as you planned.
- Pricing amounts are yours to decide. These are directions only.

### Marketing targets (persistent places)

1. **Lospec Software directory**: https://lospec.com/software/ — anyone can "Submit Software Page"; pixel-art audience browsing for tools. Claim the page as developer to post update notices to followers.
2. **ellisonleao/magictools** (GitHub), the best-known gamedev tools list: https://github.com/ellisonleao/magictools — open a PR adding Sprite Gibber under Graphics/Animation. Similar lists: https://github.com/mbrukman/awesome-game-dev and https://github.com/substain/tools-for-gamedev (free-tools focus; it lists paid tools too, and the MIT source qualifies).
3. **itch.io tools section**: publish as Kind "Tool", classification "Tools", and use the tags below. itch's tool browse pages (`itch.io/tools/tag-pixel-art`, `tag-sprites`, `tag-animation`) are where devs actively shop.
4. **OpenGameArt.org**: post a free CC0 sample pack of gibbed animal spritesheets made with the tool, with a link in the description. Asset browsers become tool users.
5. **AlternativeTo**: https://alternativeto.net/ — add Sprite Gibber as an alternative to Pixel Composer / particle and VFX tools. Low effort, indexed by search engines, permanent.

---

## itch.io

### Name of project

Sprite Gibber

### Subtitle (100 characters max)

Turn any pixel art sprite into an exploding gib animation. 479 presets, PNG frames, spritesheet, GIF

### Long description (markdown)

```markdown
# Sprite Gibber

**This is a windows program that turns any pixel art sprite into a death/destruction animations in a single click, purely using code.**

Drop in your sprite PNGs, pick a preset, and Sprite Gibber blows them apart into tumbling, spinning, gravity-driven chunks. Then it exports ready-to-use **frame PNGs**, a **spritesheet** and an **animated GIF**. No animation skills, no frame-by-frame drawing, unlimited, standalone, fast and automates entire folders worth of sprites.

## 479 presets, 61 effect types

While you can make your own effects very easily, I've gone through the effort of making many ready-to-use presets for you:

Fire, cryo, electric, plasma, water, acid, blood, meat, bone, rot, plague, stone, gold, crystal, rust, goo, sand, smoke, ash, glitch, matrix, holy, arcane, shadow, singularity, nuclear, antimatter and many more. 

Each comes in variations for different settings: falling and piling up on the ground, floating underwater, crushed inward, drifting in zero gravity, blasted sideways, or bursting from within.

You can use them as-is, edit them, create new presets from scratch or even press a "Randomize" button to create an infinite amount of new effects to try. You can even finetune the randomizion to lock-on to the traits you want to keep.

## Features

- **Live animated preview**: see every change play on your sprite immediately
- **Searchable preset library**: type "fire" or "space" to filter, click to apply
- **Batch export**: tune one sprite, then export your whole sprite list in one go
- **Full control when you want it**: chunk count, blast modes (explode, implode, shatter, split…), gravity direction and modes (vortex, orbital, repulsor…), drag, spin, bounce
- **Wound tint**: colour bleeding in from the cracks or glowing out from the core, with animated colour shifts (ignite → char, flesh → bone, raw → rust)
- **Dissolve**: pixels fade out in patterns (noise, directional, from the centre, whole chunks) with a colour flash before they vanish
- **Frame masks**: cut the animation into shapes (circles, stars, gears, runes)
- **Save your own presets** and a randomizer to discover new looks
- **Clean output**: transparent PNGs at your sprite's canvas size, spritesheets with configurable rows, crisp upscaled GIFs

## Who it's for

Indie devs, game jammers and pixel artists who need lots of good-looking death/break/destroy animations without hand-animating every enemy, crate and prop. 

You can give the animations to practically anything; be it characters, ghosts, bullets, objects, fireballs, projectiles, grenades, vases, boxes, skeletons, fruits, bread or meatloaves. And the best part its all very easy and fast.

## How to use

1. Unzip, run `SpriteGibber.exe` (Windows, no install)
2. Add your sprites (transparent PNG, pixel art, sizes from 8x8px to 512x512px and above is supported)
3. Pick a preset, watch the preview
4. Export, and the files appear in a `gibbed/` folder next to your sprites

A full guide (`guide.md`) is included and opens from the **Help Guide** button in the app.

---

Check out everything else I do: ✨🚀
https://linktr.ee/reactorcore

-Reactorcore
```

-snipped out-
The source code is also available on GitHub under the MIT license, for anyone who wants to tinker. Buying this build is the easy way to use it and directly supports development.


### Tags (10, comma separated)

pixel-art, sprites, animation, gamedev, game-assets, death-animation, explosion, spritesheet, vfx, tool

---

## GitHub

### Description blurb

Turn pixel art sprites into exploding gib/death animations: 479 presets, live preview, exports frame PNGs, spritesheets and GIFs. Python + Tkinter, Windows exe.

### Topics (10, one per line)

pixel-art
sprite-animation
gamedev
game-development-tools
spritesheet
procedural-animation
voronoi
physics-simulation
python
tkinter

---

## YouTube (showcase / trailer)

### Title

Sprite Gibber: Turn Any Pixel Art Sprite Into a Gib Animation (Destroy Anything)

### Description

```
Sprite Gibber is a windows program for game developers or animators that lets them explode any pixel-art sprites in endless cool elemental ways - usually for use as death/destruction animations. Theres stuff like fire, ice, blood, acid, gold, glitch, nuclear and many many more - 479 presets in total in 61 categories + infinite more that you can custom make or randomize with a single click. 

To use it, you just drop in your sprite PNGs, pick a preset, watch the live preview, and export frame PNGs, a spritesheet and an animated GIF.

Made for the layperson developer, unlimited, standalone, automatic and fast.

Get it: https://reactorcore.itch.io/sprite-gibber

Made by Reactorcore

Contact: reactorcoregames@gmail.com

Check out everything else I do: ✨🚀
Home/Links: https://linktr.ee/reactorcore
Releases: https://reactorcore.itch.io
Blog: https://www.patreon.com/ReactorcoreGames
Discord: https://discord.gg/UdRavGhj47
Catalog: https://reactorcoregames.github.io/

-Reactorcore
```

(Swap in the exact itch.io page and GitHub repo URLs once they're live.)

### Tags (comma separated)

pixel art, sprite animation, gamedev, indie dev, death animation, explosion effect, gibs, spritesheet, game assets, pixel art tool, vfx, game jam, procedural animation, game dev tools


## Discord post

Sprite Gibber: Destroy Anything (easy sprite animation tool)

Trailer: https://www.youtube.com/watch?v=sHdlQD-692o
Release: https://reactorcore.itch.io/sprite-gibber

This is a windows program that turns any pixel art sprite image into a cool death/destruction animation in a single click. Purely code-driven, standalone, unlimited, fast and comes with hundreds of ready presets!

You can give the animations to practically anything; be it characters, ghosts, bullets, objects, fireballs, projectiles, grenades, vases, boxes, skeletons, fruits, bread or meatloaves. And the best part its all very easy and fast.