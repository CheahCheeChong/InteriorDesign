# InteriorDesign

Public working repo used by Claude to host images that need a public URL
(for example as input to Recraft image-to-image), plus the scripts that
produced them. Everything here is intentionally public.

## Project: 3-bedroom ~1100 sqft condo, warm Japandi style

- Layout: mirrored version of the developer floor plan, wall + door between
  kitchen and yard removed. Bedroom 3 is L-shaped (wraps above the common
  bath) with its door on the hallway wall beside Bedroom 2's. Main entrance
  door sits on the dining/corridor wall, in line with the kitchen glass door.
- Kitchen windows are on the old yard wall (west wall, x=100, y 12-108,
  z 40-88), NOT on the south wall above the sink. The south wall is solid
  with a full run of cream upper cabinets over the sink.
- Corner unit, extra exterior windows: Bedroom 3 south wall (y=120, x 20-80),
  Bedroom 2 wall facing the AC ledge (y=348, x 14-50), master bedroom west
  wall (x=62, y 460-525). Common bath window is on its kitchen-facing wall
  (y=120, x 110-142, high louvre), not on the hallway wall. No aircond unit
  above the Bedroom 2 door.
- Source model: SketchUp file `D1220.skp` (built via the
  Trimble SketchUp connector). Units in the scripts are inches.
- Palette: warm oak + walnut, oatmeal boucle, linen, rattan, brushed brass,
  terracotta/rust and olive accents, warm-white walls, terrazzo kitchen floor.

## Folders

- `renders/` – Blender Cycles renders of the real model (camera angles below).
- `photoreal/` – Recraft image-to-image results made from `renders/`.
- `scripts/build_house_render.py` – self-contained Blender script: rebuilds
  the model, materials, lights, cameras, and renders every view.
  NOTE: it predates v3 and still has the old south-wall kitchen windows;
  re-export the geometry from v3 before re-rendering the kitchen.

## Workflow for "make a realistic image of room X"

1. Render the angle from the actual model in Blender on the user's Mac
   (Blender 5.2). Run in Blender's Python console:
   `exec(open('/Users/cheahcheechong/Desktop/House_Render/<script>.py').read())`
   - Use the CPU device. Metal GPU kernel compile hangs on this machine.
   - Render via `bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)`
     with a `render_complete` handler; a blocking render freezes the UI.
   - Quick test: 960x540 / 24 samples (~20 s). Final: 1600x900 / 96 samples
     (~4–5 min per view).
2. Commit the render to `renders/` here and use its raw URL:
   `https://raw.githubusercontent.com/CheahCheeChong/InteriorDesign/main/renders/<file>.jpg`
3. Recraft `image_edit` (default model nano_banana_2, ~11 credits per image)
   with that URL and a prompt that says "keep the exact same camera angle,
   layout and every piece of furniture; do not add, remove or move anything;
   only upgrade materials and lighting", then list the room's materials.
   - Do NOT use `image_to_image` for this: even at strength 0.45 it rearranges
     the room (moved the sofa, invented a kitchen).
   - nano_banana_pro is not on the user's plan.
4. Record the result links in `photoreal/README.md`.

Notes: direct uploads to mcp.recraft.ai and GitHub gists are blocked from
Claude's sandbox; this repo is the workaround.

## Camera views (inches, model coords; X east, Y north, Z up)

| View | Eye | Target | HFOV |
| --- | --- | --- | --- |
| 01 Living from dining | (302, 203, 56) | (240, 470, 44) | 76° |
| 02 Dining from living | (300, 470, 58) | (238, 262, 40) | 80° |
| 03 Kitchen | (232, 178, 62) | (170, 30, 40) | 84° |
| 04 Master bedroom | (70, 505, 58) | (186, 478, 44) | 88° |
| 05 Overview (no ceiling) | (170, -330, 640) | (170, 290, 0) | 52° |

## Keeping room size and walls (lesson from kitchen + master bedroom)

nano_banana_2 tends to zoom out, enlarge small rooms and drop walls that fill
part of the frame. The user confirmed the model sizes are correct, so prompts
must forbid this explicitly, e.g.:

"Photorealistic retouch of this exact image. This is a SMALL, compact room:
keep the identical framing, crop, camera position, lens and perspective. Do
NOT zoom out, widen the view, make the room bigger or add floor space. Keep
the plain wall that fills the right side of the frame. Every object keeps its
exact position, size and outline: <list objects by frame position>. Only
replace materials and lighting with realistic ones: <materials>."

- gemini_25_flash_image (5 credits) keeps the layout but adds little realism.
- Kitchen render 03 has a wall filling the right half; consider re-rendering
  from a clearer angle rather than relying on the prompt.

## SketchUp connector save budget (30 saves per account; 6 used as of D1220)

Only `save_model` costs a save; `build_model` calls and rebuilding after a
session timeout are free. Rules:
1. Batch every requested change into one round, then save once.
2. Before saving, verify with a free preview: export geometry via
   `build_model` and draw a top-down plan / quick view here, show the user,
   and save only after they confirm.
3. Save only when the user needs the .skp (to open it or render from it).
4. Sessions expire after ~30 min idle; rebuild from the build steps (free),
   then save once at the end.
5. For heavy iteration, offer a Ruby Console script for the user's own
   licensed desktop SketchUp (no save limit).

## File version compatibility

The SketchUp connector always saves in SketchUp 2026 format (header {26.1.0});
the user's desktop SketchUp is 2022 and cannot open those files. For a file
the user can open, export the model tree from the connector session and use
`scripts/D1220.rb`: open a new model in the user's SketchUp, then in
Window > Ruby Console run
`load "/Users/cheahcheechong/Desktop/House_Render/D1220.rb"`
and File > Save As. This costs no connector saves.
