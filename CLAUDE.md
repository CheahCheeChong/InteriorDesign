# InteriorDesign

Public working repo used by Claude to host images that need a public URL
(for example as input to Recraft image-to-image), plus the scripts that
produced them. Everything here is intentionally public.

## Project: 3-bedroom ~1100 sqft condo, warm Japandi style

- Layout: mirrored version of the developer floor plan, wall + door between
  kitchen and yard removed. Bedroom 3 is L-shaped (wraps above the common
  bath) with its door on the hallway wall beside Bedroom 2's. Main entrance
  door sits on the dining/corridor wall, in line with the kitchen glass door.
- Source model: SketchUp file `My_House_Warm_Style_v2.skp` (built via the
  Trimble SketchUp connector). Units in the scripts are inches.
- Palette: warm oak + walnut, oatmeal boucle, linen, rattan, brushed brass,
  terracotta/rust and olive accents, warm-white walls, terrazzo kitchen floor.

## Folders

- `renders/` – Blender Cycles renders of the real model (camera angles below).
- `photoreal/` – Recraft image-to-image results made from `renders/`.
- `scripts/build_house_render.py` – self-contained Blender script: rebuilds
  the model, materials, lights, cameras, and renders every view.

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
