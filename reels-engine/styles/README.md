# Animation style library

34 reusable animation styles, studied from Donte's reference reels (Nov 2026). Each style is one page in `s/` that exposes `window.render(t)` (seconds) and `window.DUR`, sets `window.READY=true`, and is drawn at 1080×1920. Rendering is deterministic: no `Math.random` (use `rng(seed)` from `s/lib.js`), no `Date`, no network beyond files in this folder.

## Render a style clip
```
cd reels-engine/styles
npm install                      # three, world-atlas, topojson-client
python3 -m http.server 8765 &    # pages load modules over http
python3 render.py ink_wash stained_glass      # -> out/<name>.mp4  (Playwright Chromium + ffmpeg)
python3 snap.py ink_wash 1 2.5 4               # -> frames/ink_wash_strip.png
```
`render.py` launches Chromium with SwiftShader WebGL flags so the 3D styles work headless. Times: 2D ~10-30 s a clip, 3D ~30-120 s, toy_miniature ~5 min.

## Editing
The pages are generated: edit the Python builder, then run it. `mk.py` holds the page template (`page(name, bg, js, css, html)`).
- `build_office_styles.py` – shared 3D office scene (`s/office.js`): thermal, hologram, cyberpunk, claymation, blueprint (isometric is hand-written in `s/isometric.html`)
- `build_a.py` particle, stained_glass, neon, low_poly · `build_b.py` paper_cutout, watercolor · `build_c.py` liquid_chrome, toy_miniature, black_hole, teardown
- `build_d.py` the 14 business blocks (map_route, stat_chart, headline, paper_desk, before_after, iso_flow, notifications, day_counter, rent_vs_buy, bar_chart, social_card, app_mockup, globe_arcs, laptop_reveal)
- `build_fix.py` (run last) – the Nov 18 reworks: ascii, crystal_glass, ink_wash, ukiyo_e

## Approved for use (Donte, Nov 18 2026)
- **Parables for Builders:** `ink_wash`, `stained_glass`, `paper_cutout`, `claymation`. **Not** `ukiyo_e` (reads as AI-made).
- **Real-estate / landlord reels:** `rent_vs_buy`, `notifications`, `iso_flow` (step flow), `stat_chart`, `before_after`, `day_counter`.
- Everything else is a reference to borrow techniques from, not a look to post as-is.

## Not built yet (hard)
Anime cel, origami that folds itself, walking characters, true hand-painted texture.

## Using a style in a Parables episode (HyperFrames, `../hf/`)
The episode stays a HyperFrames file (`hf/epNN_slug.html`) so the voice cueing (`K.at`), captions, hook card, header and cream ending stay the same. The style replaces the story drawing between the hook card and the cream page:
- Port the style's drawing code into the episode's `@html/@css/@js` (canvas or SVG layer inside the objects area, y 560-1300), driven from the GSAP timeline instead of `render(t)`: add a tween on a proxy object `{t:0}` and redraw on its `onUpdate`. Three.js pages need the same WebGL Chrome flags `render.py` uses.
- Keep the episode's own objects and labels (short Inter caps), cued to the spoken words; the style is how they are drawn, not a separate clip.
- Background colour, light beams, grain: use the style's own palette for the story section (ink wash = paper `#efe8d8`, stained glass = dark stone `#120a06`, paper cutout = warm paper, claymation = warm tan); header, captions and the cream ending keep the series colours.
