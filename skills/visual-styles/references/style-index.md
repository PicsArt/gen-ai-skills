# Style index

One row per style the picker offers. `id` is the recipe id: fetch it with `picsart_scene_recipe`
(`name: "visual-styles"`, `reference: "references/<id>.md"`). `previewUrl` is the 3-second loop shown on the
tile.

- `category`: one of nine names (Cartoon & TV, Anime & Manga, Paper, Clay & Craft, Ink & Sketch, Pop & Print, Retro & Neon,
  Explainers & Data, Toy, 3D & Technical, Screen & Broadcast), at most 40 characters, on every row. A style board passes it
  as the `category` of each card, and the picker groups the cards under chips.

The four columns `words`, `rows`, `cast` and `score` apply to film rows only, and say how a film in that style is
planned; an empty cell takes the defaults in [the film flow](film-flow.md), and the graphic rows leave them empty.

- `words`: how the plan's words reach the viewer, comma-separated from `voice-over`, `lip-sync`, `captions`
  (which also covers speech balloons), `intertitles` and `sound-words` (drawn words for sounds); `none` is a style
  with no words.
- `rows`: what a row of the plan is: `shots`, `panels` or `drawing` (one drawing cut by bars).
- `cast`: `rig` builds a rig; `shapes` draws the figures without one; `pictures` cuts every character from
  generated pictures into a puppet; `poses` draws every key pose as its own whole picture and cuts from one to the
  next, with no puppet and no in-between.
- `score`: `first` plans the sound before the picture, `last` after it.

| id | label | category | use | words | rows | cast | score | notes | previewUrl |
|---|---|---|---|---|---|---|---|---|---|
| `classic-cartoon` (default) | Classic cartoon | Cartoon & TV | film |  |  |  |  | thick outlines, flat bright colour, bouncy friendly motion | https://pcdn.picsart.com/templates-cdn/d511fc64-1742-40e5-80e3-fbdca676fbdb.mp4 |
| `simple-shapes` | Simple shapes | Cartoon & TV | film |  |  | shapes |  | primitive shapes under one even slate line, flat colour, the shape-built rig acting | https://pcdn.picsart.com/templates-cdn/751654e5-6009-4edb-8183-3a5f407f91a0.mp4 |
| `lofi-room` | Lofi room | Cartoon & TV | film |  |  | shapes |  | a lamp-lit night room: a reader in an armchair, rain on the window, a steaming cup, swaying plants, a seamless slow loop | https://pcdn.picsart.com/templates-cdn/5a75dc5b-e962-49f0-848b-b16c60fb26c0.mp4 |
| `kid-show` | Kid show | Cartoon & TV | film |  |  | pictures |  | a cartoon for young children cut from pictures: thin coloured lines, soft cel shading, big friendly eyes, bright clear colour | https://pcdn.picsart.com/templates-cdn/6c9624e0-9171-4bd5-b630-11e10887cf39.mp4 |
| `cel-anime` | Cel anime | Anime & Manga | film |  |  |  |  | flat summer skies, two-tone clouds, wind in the grass | https://pcdn.picsart.com/templates-cdn/c890ad7b-5d8d-4908-9ca5-940e67c9e7ae.mp4 |
| `painted-anime` | Painted anime | Anime & Manga | film |  |  |  |  | hand-painted film backgrounds in depth, cel-shaded characters walking through them | https://pcdn.picsart.com/templates-cdn/a2b8e08c-9086-4a8d-83dd-69ba1063f6dd.mp4 |
| `retro-anime` | Retro 90s anime | Anime & Manga | film |  |  | pictures |  | hand-painted cels shot on film: muted warm colour, soft lines, glowing highlights, grain, a weaving 4:3 picture | https://pcdn.picsart.com/templates-cdn/6a7618bd-4935-4bcd-82d1-dade4fe9d4f8.mp4 |
| `pastel-anime` | Pastel anime | Anime & Manga | film |  |  | pictures |  | pastel anime characters cut from pictures, thin tinted lines, soft cel shading, star and sparkle magic | https://pcdn.picsart.com/templates-cdn/e0034196-8d54-4e7a-aab4-650f02f30c94.mp4 |
| `action-anime` | Action anime | Anime & Manga | film |  |  | poses |  | bold dark outlines, hard two-tone shading, drawn key poses held between fast moves, speed lines, impact frames and camera shake | https://pcdn.picsart.com/templates-cdn/2704f269-6a8d-4e1d-8d54-be421cad50f6.mp4 |
| `chibi-anime` | Chibi anime | Anime & Manga | film |  |  | pictures |  | tiny big-headed characters cut from pictures, a bold round line, snappy squash and stretch, reaction marks on a flat colour card | https://pcdn.picsart.com/templates-cdn/d5b5b301-5aac-436b-8f08-ee55c561aa5c.mp4 |
| `watercolour-anime` | Watercolour anime | Anime & Manga | film |  |  | pictures |  | anime characters and places in pale watercolour washes, soft pencil lines, paper showing, slow drifting motion | https://pcdn.picsart.com/templates-cdn/b4043214-ea8d-4a59-a1c1-d9df406c6989.mp4 |
| `night-city-anime` | Night-city anime | Anime & Manga | film |  |  | pictures |  | neon signs over a wet street, rain, picture characters graded for night with a coloured rim | https://pcdn.picsart.com/templates-cdn/f6b58545-7985-471c-92ee-4b15881370db.mp4 |
| `rubber-hose` | Rubber hose | Cartoon & TV | film |  |  | shapes |  | black-and-cream ink, tube limbs, everything bounces on the beat | https://pcdn.picsart.com/templates-cdn/47041f8c-be2c-4d51-b9f7-070bd974c8e8.mp4 |
| `cut-paper` | Cut paper | Paper, Clay & Craft | film |  |  | shapes |  | textured paper layers, stop-motion bounce | https://pcdn.picsart.com/templates-cdn/1c87d882-6d46-431b-a304-32b81806d2c7.mp4 |
| `paper-playhouse` | Paper playhouse | Paper, Clay & Craft | film |  |  | shapes |  | a snowy-night paper theatre: curtains part, flats slide in from the wings, a puppet fox on a rod crosses the stage in a warm pool of light, soft shadows and a slow push | https://pcdn.picsart.com/templates-cdn/f00abe4a-a854-4143-96c2-51d890f9b49c.mp4 |
| `watercolour-storybook` | Watercolour storybook | Paper, Clay & Craft | film | captions |  |  | first | dusk washes with soft bleeding edges, a wobbling ink line, added window light, lyric words filling on the beat | https://pcdn.picsart.com/templates-cdn/8b49356c-f3f9-4182-8bfa-7ea2e3e3a445.mp4 |
| `shadow-puppet` | Shadow puppet | Paper, Clay & Craft | film |  |  | shapes |  | black silhouettes against a warm lit screen | https://pcdn.picsart.com/templates-cdn/95c3089e-cd01-4ccf-9a03-6aac5b61a44d.mp4 |
| `manga-panels` | Manga panels | Anime & Manga | film | captions, sound-words | panels |  |  | black-and-white panels, screentone, speed lines, sound effects | https://pcdn.picsart.com/templates-cdn/e73a5447-9081-4091-89e2-fe3c2b292530.mp4 |
| `midcentury-toon` | Mid-century toon | Cartoon & TV | film |  |  | shapes |  | angular figures, flat retro shapes, mustard and teal | https://pcdn.picsart.com/templates-cdn/d6161282-641d-4359-bb56-efd3c5da20bb.mp4 |
| `silhouette-rhythm` | Silhouette rhythm | Paper, Clay & Craft | film | captions | drawing | shapes | first | black shapes on bold colour fields that switch with the beat | https://pcdn.picsart.com/templates-cdn/d543fba6-7887-4b87-97ba-1afc761b023c.mp4 |
| `retro-future-toon` | Retro-futurism | Cartoon & TV | film |  |  | shapes |  | dusk planet, atom-sign house, saucer and rocket in ink and flat colour | https://pcdn.picsart.com/templates-cdn/8cfb26e6-6588-4830-a28a-fcfc8afb2209.mp4 |
| `pop-up-book` | Pop-up book | Paper, Clay & Craft | film |  |  |  |  | paper scenery folds up off an open book, camera sways | https://pcdn.picsart.com/templates-cdn/0937d1b5-bc8f-4546-826c-681e6f50b8f0.mp4 |
| `clay-on-twos` | Clay animation | Paper, Clay & Craft | film |  |  | shapes |  | soft plasticine lumps, trembling outline, held every second frame | https://pcdn.picsart.com/templates-cdn/2848eae5-e1a9-4b51-a346-77967d915bd1.mp4 |
| `silent-reel` | Silent film | Cartoon & TV | film | intertitles |  | shapes |  | grey slapstick with iris, intertitle, flicker and scratches | https://pcdn.picsart.com/templates-cdn/278be1ad-dbe3-4141-9412-47c10ab3cac1.mp4 |
| `one-line` | Continuous line | Ink & Sketch | film |  |  | shapes |  | a single unbroken ink line draws the picture and erases itself | https://pcdn.picsart.com/templates-cdn/7db45122-e998-43df-b08b-e0b17e9230ac.mp4 |
| `stick-figure` | Stick figure | Cartoon & TV | film |  |  | shapes |  | stroke-only figures, round heads, plain coloured ground, slapstick action | https://pcdn.picsart.com/templates-cdn/d1eeade9-7e14-4fa8-9c25-1b65510c3063.mp4 |
| `stained-glass` | Stained glass | Paper, Clay & Craft | film |  |  | shapes |  | jewel panes between lead, lit from the centre, beams and glare | https://pcdn.picsart.com/templates-cdn/faffcd06-aaa2-497b-9bc8-feb4d9394f33.mp4 |
| `woodblock-print` | Woodblock print | Ink & Sketch | film |  |  | shapes |  | graded sky, red sun, flat blues, scale-wave sea | https://pcdn.picsart.com/templates-cdn/7c5808cb-0837-425b-ac99-477074945c7f.mp4 |
| `ink-wash` | Ink wash | Ink & Sketch | film |  |  | shapes |  | grey washed hills with one heavy brush edge on warm paper, drifting mist, a red sun, a boat bobbing, a swallow, willows swaying | https://pcdn.picsart.com/templates-cdn/77a22c73-43f6-4336-887a-9c2f7d9dfa09.mp4 |
| `woodblock-cartoon` | Woodblock cartoon | Ink & Sketch | film |  |  | pictures |  | a cartoon as a series of Japanese colour woodblock prints: still printed poses swapped and held, a walk of a few drawings with planted feet, flat colour in a bold line, cloth patterns, graded skies, one red | https://pcdn.picsart.com/templates-cdn/1123d039-f058-4409-92c4-bf703fd1fb35.mp4 |
| `stick-explainer` | Whiteboard explainer | Explainers & Data | film |  |  | shapes |  | stick figure, idea bulb, arrow and chart drawn on | https://pcdn.picsart.com/templates-cdn/577f59b2-36d5-40be-9c66-cfd4f88fd9b0.mp4 |
| `woodcut` | Woodcut | Ink & Sketch | film |  |  | shapes |  | black ink block with tapered white gouge marks, carved in by steps | https://pcdn.picsart.com/templates-cdn/79f7d04e-c029-4b14-9178-49d22b5775c1.mp4 |
| `line-boil-sketch` | Line-boil sketch | Ink & Sketch | film |  |  |  |  | pencil outlines that wobble each frame, drawn stroke by stroke | https://pcdn.picsart.com/templates-cdn/36297a22-6eb7-488a-86a3-262a45ad905f.mp4 |
| `brick-toy` | Brick stop-motion | Toy, 3D & Technical | film |  | shots | shapes |  | glossy studded bricks on a wooden desk, macro focus, figures on twos (3D) | https://pcdn.picsart.com/templates-cdn/65c9c269-e431-484a-bc40-f19768dc24aa.mp4 |
| `blocky-world` | Blocky world | Toy, 3D & Technical | film |  | shots | shapes |  | a world of 1 m blocks with crisp 8×8 texels: teal turf, orange soil, hard sun shadows, a slow camera over stepped terrain, with two walking characters (3D) | https://pcdn.picsart.com/templates-cdn/ea563ba0-83e8-4f4d-a2c9-1c1ced1dc2cb.mp4 |
| `picture-cutout` | Picture cut-out | Paper, Clay & Craft | film |  |  | pictures |  | generated pictures cut along their own edges, puppets on joints, a set that drifts and sways | https://pcdn.picsart.com/templates-cdn/82345a09-639b-4600-8519-b673beb1b390.mp4 |
| `flat-ink-cast` | Flat ink cast | Cartoon & TV | film |  |  |  |  | one thick even black line, flat muted fills, calm held acting on twos, a loud red accent | https://pcdn.picsart.com/templates-cdn/12398a5d-327d-48ae-a80a-885aef40ddde.mp4 |
| `swiss-grid` | Swiss grid | Pop & Print | graphic |  |  |  |  | hairline grid, one red circle, snapping moves, huge flush-left type | https://pcdn.picsart.com/templates-cdn/0d601d9f-1303-48a2-a463-854b387c0e17.mp4 |
| `pictogram` | Pictogram | Explainers & Data | graphic |  |  |  |  | one repeated icon counts in, one row changes colour, bars grow | https://pcdn.picsart.com/templates-cdn/b9e8819a-bdac-42df-9bbd-8574dc167f95.mp4 |
| `bauhaus-poster` | Bauhaus poster | Pop & Print | graphic |  |  |  |  | circle, square, half circle, bars, a heavy grotesque, a final quarter turn | https://pcdn.picsart.com/templates-cdn/56716f50-e366-47bc-93c2-815c315a6f10.mp4 |
| `deco-title` | Deco title | Pop & Print | graphic |  |  |  |  | gold on navy, fanned rays, stepped frame, shimmer on the letters | https://pcdn.picsart.com/templates-cdn/ba768410-c326-49b4-976f-d8c53c39a1c1.mp4 |
| `memphis-pop` | Memphis pop | Pop & Print | graphic |  |  |  |  | pastels, squiggles, blobs, confetti, heavy outlined type | https://pcdn.picsart.com/templates-cdn/46f9bf2a-f5b7-4d9a-9a2e-1e7c6b2481e8.mp4 |
| `popart-burst` | Pop-art burst | Pop & Print | graphic |  |  |  |  | Ben-Day dots, primary colours, action lines, one loud DING | https://pcdn.picsart.com/templates-cdn/a0a8a23e-0e33-4d10-98a2-9656b3fdd21c.mp4 |
| `comic-panels` | Comic panels | Pop & Print | graphic |  |  |  |  | tinted dotted panels, balloons, a story across three panels | https://pcdn.picsart.com/templates-cdn/f49d3ddf-1bea-4b36-892e-bca4d65e6339.mp4 |
| `silkscreen` | Silkscreen | Pop & Print | graphic |  |  |  |  | two inks multiply, off-register plates, stipple edges | https://pcdn.picsart.com/templates-cdn/4568e9e6-cff5-4845-a49d-3196dd3cd945.mp4 |
| `riso-overprint` | Riso overprint | Pop & Print | graphic |  |  |  |  | pink and blue overprint, speckled edges, stepped misregistration | https://pcdn.picsart.com/templates-cdn/d847bca8-62a5-4b98-92d9-65b5263250f5.mp4 |
| `print-dossier` | Print dossier | Pop & Print | graphic |  |  |  |  | an archive sheet toned in dots, two spot inks overprinting, tabs, a reference line and a red stamp that slams in | https://pcdn.picsart.com/templates-cdn/cf53b3ab-f3c2-4a0d-98c6-d48c77563fdd.mp4 |
| `silhouette-titles` | Silhouette titles | Pop & Print | graphic |  |  |  |  | a red field, a cream moon, black jagged-cut figures and pines, a walking figure and dog, crows and a chunky stencil word | https://pcdn.picsart.com/templates-cdn/19d824e3-eded-4b5e-aba9-1b6a8c326480.mp4 |
| `one-bit-dither` | One-bit dither | Retro & Neon | graphic |  |  |  |  | greys drawn first, then noise and levels give a dither | https://pcdn.picsart.com/templates-cdn/576e5db2-7891-460e-beab-b30b73c40677.mp4 |
| `neon-tubes` | Neon tubes | Retro & Neon | graphic |  |  |  |  | white-core tubes, glow, stuttering flicker, a pink cat | https://pcdn.picsart.com/templates-cdn/ffd3ede1-e032-43bf-bc60-d436d6240d3c.mp4 |
| `synthwave` | Synthwave | Retro & Neon | graphic |  |  |  |  | striped sun, neon grid rolling toward you, wire mountains, chrome title | https://pcdn.picsart.com/templates-cdn/750acd0a-b541-4850-a10a-e6f7d74e06fa.mp4 |
| `y2k-gloss` | Y2K gloss | Retro & Neon | graphic |  |  |  |  | fat aqua gel letters, a chrome ring, rising bubbles, a pink jelly icon, a cut orange sun over a grid floor | https://pcdn.picsart.com/templates-cdn/635ed09c-689a-46da-a3dc-18c00e64220d.mp4 |
| `vhs-tape` | VHS tape | Retro & Neon | graphic |  |  |  |  | split red/green/blue title, tape noise, scanlines, a PLAY mark, glitch bursts | https://pcdn.picsart.com/templates-cdn/c57b867a-19c7-4040-ac5a-101647b1e283.mp4 |
| `goo-blobs` | Goo blobs | Retro & Neon | graphic |  |  |  |  | blur and threshold merging blobs, a gradient tint, a glass outline | https://pcdn.picsart.com/templates-cdn/1e6afc68-4f06-4476-8f74-3cb362788e84.mp4 |
| `firefly-night` | Firefly night | Retro & Neon | graphic |  |  |  |  | particle fireflies, one glow, hills and foreground blades | https://pcdn.picsart.com/templates-cdn/834f009c-73be-4986-a60c-a4db9d35e34e.mp4 |
| `chalkboard` | Chalkboard | Ink & Sketch | graphic |  |  |  |  | chalk strokes with stipple, outlines only, handwritten labels | https://pcdn.picsart.com/templates-cdn/824ab049-e4ec-43c4-aa31-0d4538348ae0.mp4 |
| `pen-plotter` | Pen plotter | Ink & Sketch | graphic |  |  |  |  | one ink, hatch by repeater, clipped passes, drawn pass by pass | https://pcdn.picsart.com/templates-cdn/ca753dde-f585-4a3f-b1a3-6138e9c64607.mp4 |
| `paper-map-comic` | Paper map comic | Paper, Clay & Craft | graphic |  |  |  |  | a comic page of cut-paper countries, a lighter patch slapped over a border, a stamp, panels that slide, a paper puppet with a bubble | https://pcdn.picsart.com/templates-cdn/d0b0a425-c945-4be0-ba61-229ec7c4d72a.mp4 |
| `layered-lightbox` | Layered lightbox | Paper, Clay & Craft | graphic |  |  |  |  | paper sheets darker toward the front over a bright back glow, soft cast shadows, warm windows, a dolly that separates the sheets | https://pcdn.picsart.com/templates-cdn/0434df63-0b9d-4734-b338-e911e859e4d4.mp4 |
| `paper-fold` | Paper fold | Paper, Clay & Craft | graphic |  |  |  |  | hinged flaps, perspective turn, motifs revealed edge-on | https://pcdn.picsart.com/templates-cdn/c7a7ed29-5f73-45f4-82b4-6b53389a70ef.mp4 |
| `kinetic-type` | Kinetic typography | Pop & Print | graphic |  |  |  |  | one word per beat, flipping palettes, punch zoom, a stacked lockup | https://pcdn.picsart.com/templates-cdn/ad354057-2a2c-4a99-84ee-241a852c0b7f.mp4 |
| `space-explainer` | Space explainer | Explainers & Data | graphic |  |  |  |  | navy sky, ringed planet, one red rocket, path-following craft | https://pcdn.picsart.com/templates-cdn/bf3970f8-1a87-492d-a1c8-70a140fb9df7.mp4 |
| `glow-explainer` | Glow explainer | Explainers & Data | graphic |  |  |  |  | flat shapes on navy, soft glows, small bean-shaped people, one zoom across scales | https://pcdn.picsart.com/templates-cdn/78eed0c4-1f4b-4bb5-8cf4-0f5a89f12f2f.mp4 |
| `isometric-town` | Isometric town | Toy, 3D & Technical | graphic |  |  |  |  | three-tone blocks, 2:1 projection, depth order by z, one warm car | https://pcdn.picsart.com/templates-cdn/5b93a53e-57c0-417d-9af4-2cd1e9f777cb.mp4 |
| `tilt-shift-town` | Tilt-shift town | Toy, 3D & Technical | graphic |  |  |  |  | a miniature toy city seen from above (a real 3D scene): pastel blocks, cars looping, a light sweeping across the day, a sharp middle strip with blurred top and bottom, a running clock | https://pcdn.picsart.com/templates-cdn/484546d1-3cda-42fe-9971-61224f3c1606.mp4 |
| `transit-map` | Transit map | Explainers & Data | graphic |  |  |  |  | 45-degree lines, one colour per line, interchange hubs, running trains | https://pcdn.picsart.com/templates-cdn/2adfa0d0-7fed-45cd-886a-e40d15b45584.mp4 |
| `route-map` | Route map | Explainers & Data | graphic |  |  |  |  | soft sea and land, red dashed route, pins, camera pans, fixed title | https://pcdn.picsart.com/templates-cdn/69e66412-00a8-4424-b54a-28a7c77f79d6.mp4 |
| `contour-trail` | Contour trail | Explainers & Data | graphic |  |  |  |  | a survey map of a walk: nested wobbly contour lines sketch on, a pale lake, a dashed red route from a start pin over a hill to a flag, small height pills | https://pcdn.picsart.com/templates-cdn/39cee6a0-a65d-4d0f-98f7-0295486362c2.mp4 |
| `soft-toy-3d` | Soft toy 3D | Toy, 3D & Technical | graphic |  |  |  |  | pastel glossy toy plastic: hex tiles popping in ring by ring, meshed gears, squashing boxes, soft lilac shadows, a swaying camera | https://pcdn.picsart.com/templates-cdn/00540e33-689d-4497-966a-c1733935eea4.mp4 |
| `blueprint` | Blueprint | Toy, 3D & Technical | graphic |  |  |  |  | white line on blueprint blue, dashed construction lines, dimensions, a swinging part | https://pcdn.picsart.com/templates-cdn/49738030-b947-4386-a28c-32436a8380f7.mp4 |
| `assembly-manual` | Assembly manual | Toy, 3D & Technical | graphic |  |  |  |  | line art, one orange accent, guides, numbered discs, quantity badge | https://pcdn.picsart.com/templates-cdn/8668bfd1-4347-4d00-8000-aa708ed20f0f.mp4 |
| `exploded-view` | Exploded view | Toy, 3D & Technical | graphic |  |  |  |  | cool greys, one amber part, staggered pull, labelled leaders | https://pcdn.picsart.com/templates-cdn/7f1cf4e0-d653-48a0-8e8b-fad278562084.mp4 |
| `factory-loop` | Factory loop | Toy, 3D & Technical | graphic |  |  |  |  | one loop period, press red, mint scan line, state change on processing | https://pcdn.picsart.com/templates-cdn/6cfb7e47-cab0-4f27-84f7-ebdb400bbccd.mp4 |
| `data-bars` | Infographic bars | Explainers & Data | graphic |  |  |  |  | grid, grey bars, one red story bar, values on tips, average line | https://pcdn.picsart.com/templates-cdn/c62f9864-0c4b-420d-ada0-7ff1b682da36.mp4 |
| `spreadsheet` | Spreadsheet | Explainers & Data | graphic |  |  |  |  | light grid, green selection, formula bar, mono type | https://pcdn.picsart.com/templates-cdn/d4d66259-05c2-48e0-870e-2c57226fcc74.mp4 |
| `sketchnote` | Sketchnote | Ink & Sketch | graphic |  |  |  |  | wobbly ink line, handwriting, line boil, yellow highlighter | https://pcdn.picsart.com/templates-cdn/ca7fcd24-9354-446b-835f-da784e1c841b.mp4 |
| `one-pen-marker` | One pen marker | Ink & Sketch | graphic |  |  |  |  | one marker on blank sheets: black for structure, blue for the facts, red for the question and answer, camera moves between sheets | https://pcdn.picsart.com/templates-cdn/8b81b202-d8f0-47f6-98fe-00450115ca94.mp4 |
| `illuminated-page` | Illuminated page | Ink & Sketch | graphic |  |  |  |  | a vellum book page written live: a red blackletter heading, a blue drop cap, lines a quill uncovers, vines growing up both margins | https://pcdn.picsart.com/templates-cdn/842d09c9-b152-4d65-bb21-9398b5ae6fa4.mp4 |
| `telestrator` | Telestrator | Screen & Broadcast | graphic |  |  |  |  | striped pitch, marker yellow, pulse ring, dashed run line | https://pcdn.picsart.com/templates-cdn/6d6756f6-50ae-4e7d-b70e-952f794f7c05.mp4 |
| `news-package` | News package | Screen & Broadcast | graphic |  |  |  |  | navy and white bars, red live badge, looping ticker, safe margins | https://pcdn.picsart.com/templates-cdn/1a53ef55-3caa-431a-b92e-40db850a7b31.mp4 |
| `gameshow-countdown` | Gameshow countdown | Screen & Broadcast | graphic |  |  |  |  | pink ring, chasing bulbs, one text layer per second, gold answer | https://pcdn.picsart.com/templates-cdn/e3a80359-0d31-4b2c-9cd2-fbf74ef42657.mp4 |
| `keynote-reveal` | Keynote reveal | Screen & Broadcast | graphic |  |  |  |  | black field, slow eases, white shine, a line of specs | https://pcdn.picsart.com/templates-cdn/38a88f81-e41e-4bb4-b216-0fedbf62a01e.mp4 |
| `terminal` | Terminal | Screen & Broadcast | graphic |  |  |  |  | dark window, orange prompt, mono text, stepped progress | https://pcdn.picsart.com/templates-cdn/039006e4-ec05-45a2-a0fc-5fd37e760ef0.mp4 |
| `device-mockup` | Device mockup | Screen & Broadcast | graphic |  |  |  |  | a bright promo: a dark phone with a habit list ticking itself off, a split ink and coral headline | https://pcdn.picsart.com/templates-cdn/8de33a05-4d26-4a32-aed2-257052f555e2.mp4 |
| `chat-thread` | Chat thread | Screen & Broadcast | graphic |  |  |  |  | a dark violet phone chat: pill bubbles popping in left and right, three-dot typing bubbles, timestamps and a message bar | https://pcdn.picsart.com/templates-cdn/401be2ea-b2a8-467a-89ec-42fd785d939b.mp4 |
| `phosphor-scope` | Phosphor scope | Screen & Broadcast | graphic |  |  |  |  | graticule, green trace with afterglow, settling readouts, flicker | https://pcdn.picsart.com/templates-cdn/dbe72cc8-a4ec-465c-a62e-4669cc59f1b7.mp4 |
| `hologram-hud` | Hologram HUD | Screen & Broadcast | graphic |  |  |  |  | one cyan at several opacities, scan band, brackets, projection flicker | https://pcdn.picsart.com/templates-cdn/843f7dad-31f6-44a4-82ce-887edf893e3e.mp4 |
| `circuit-board` | Circuit board | Screen & Broadcast | graphic |  |  |  |  | 45-degree traces, mint pulses, lit pads, glowing core | https://pcdn.picsart.com/templates-cdn/a89815f1-ab90-4d8a-b239-ad38bc0c8d0e.mp4 |
| `weather-cards` | Weather cards | Explainers & Data | graphic |  |  |  |  | sky gradient, white cards, spinning sun, drifting cloud, falling rain | https://pcdn.picsart.com/templates-cdn/7609fc7f-99c7-4ded-a1d0-b8e615d3d467.mp4 |
| `audio-ring` | Audio ring | Screen & Broadcast | graphic |  |  |  |  | cyan to violet ring, beat pulse, drifting particles, no audio input | https://pcdn.picsart.com/templates-cdn/8e950347-e6a3-43e4-944c-901c59e5ed03.mp4 |
| `mosaic-reveal` | Mosaic reveal | Retro & Neon | graphic |  |  |  |  | coarse grid, ripple start times, flip to picture, yellow origin | https://pcdn.picsart.com/templates-cdn/4750f3db-3738-4090-b5d9-570fc3e8db63.mp4 |
| `math-explainer` | Math explainer | Explainers & Data | graphic |  |  |  |  | dark board, blue curve, serif equations, yellow result | https://pcdn.picsart.com/templates-cdn/81bc6caf-d551-44f9-a863-f9282e5d91a5.mp4 |
| `station-cutaway` | Station cutaway | Explainers & Data | graphic |  |  |  |  | a production line as a cut-open building: numbered rooms, one colour per output through pipe, machine and tag, belts that never stop, a push into one room | https://pcdn.picsart.com/templates-cdn/59373ae1-f192-4a29-82a2-85ab5eec250a.mp4 |
| `flat-explainer` | Flat explainer | Explainers & Data | graphic |  |  |  |  | flat people, no outlines, popping UI cards, a chart that builds itself | https://pcdn.picsart.com/templates-cdn/6b9cf8ed-e83d-454e-a2bf-62efaae065b7.mp4 |
| `grain-editorial` | Grain editorial | Cartoon & TV | graphic |  |  |  |  | painted paper grain, no outlines, deadpan side-glancing people, one chalk word per beat | https://pcdn.picsart.com/templates-cdn/6817408f-bb84-4b5b-a55f-6f39431540b4.mp4 |
| `pixel-hop` | Pixel art | Retro & Neon | film |  |  | shapes |  | whole-pixel steps, fixed palette, twos timing, circular iris | https://pcdn.picsart.com/templates-cdn/f5182692-a058-4c17-9cd2-9558fbb86b7a.mp4 |
| `tone-on-tone-flat` | Tone-on-tone flat | Cartoon & TV | film |  |  | shapes |  | one salmon world, no outlines, big-headed noodle people, eyes that act, a camera slide | https://pcdn.picsart.com/templates-cdn/582460d8-d710-4965-884e-4b46fa0c63b6.mp4 |
| `nursery-rhyme` | Nursery rhyme | Cartoon & TV | film | captions |  | shapes |  | a vertical sing-along: one round soft-shaded SVG animal per line with big glossy eyes, soft storybook places, all painted over with oil-pastel strokes, big rounded white captions with the key word lit in yellow | https://pcdn.picsart.com/templates-cdn/6149cd5c-a6ab-4f63-acc8-41ecba59fb80.mp4 |
| `documentary-collage` | Documentary collage | Pop & Print | graphic |  |  |  |  | sepia prints taped at a tilt, sticker cut-outs, one red disc with a year, a dashed route and a stamp | https://pcdn.picsart.com/templates-cdn/45ab35fd-5ef9-434f-9fcd-b23dffa75106.mp4 |
| `dark-tech-explainer` | Dark tech explainer | Explainers & Data | graphic |  |  |  |  | near-black dot field, one glowing hero, an amber focus walking a step rail, captions in their own band | https://pcdn.picsart.com/templates-cdn/26fbd3ab-927f-43d6-9e8a-c6cbb1bf76b7.mp4 |
| `studio-reel` | Studio reel | Pop & Print | graphic |  |  |  |  | big condensed type on a ground that changes every shot, a fixed frame of corner marks with a counter, slats and an iris as transitions, one magenta slam at the end | https://pcdn.picsart.com/templates-cdn/4b3a6c48-ee94-4e87-9e1e-611360506a0a.mp4 |

## Category chips each use case shows

The picker's chips. The first chip is `Recommended`, selected on open; then one chip per name in this table, then
`Other styles` last. Every row is still on the board.

- **The table.** A cell holds the chip NAME a category takes on that use case's board; a blank cell means
  `Other styles`. Categories that share a chip name merge into one chip. This table is the one place the pairs live.
- **Minimum.** A chip needs at least 4 styles on its board (film rows for `animated-story`, graphic rows for
  `animated-explainer`). A category that would fall below 4 takes its neighbour's chip name in that use case's column;
  what is left goes under `Other styles`. A board never shows a chip with 1 to 3 cards, and a chip with no cards is
  not shown.
- **Order.** The widget orders chips by first appearance in the cards, so card order is chip order: the cards go in
  the table's chip order for that use case (the classic cartoon stays the first card on a film board), every
  `Other styles` card after all the others.
- **Recommended.** Mark 4 to 6 cards `recommended` (a request that names a style puts the named style first, 4 to 6
  in all). A picker with no recommended cards opens on its first category.
- `Other styles` and `Recommended` are board labels only, never a category in this index.

| category | animated-story | animated-explainer |
|---|---|---|
| Cartoon & TV | Cartoon & Anime | Drawn & Handmade |
| Anime & Manga | Cartoon & Anime |  |
| Paper, Clay & Craft | Paper, Clay & Craft | Drawn & Handmade |
| Ink & Sketch | Ink & Sketch | Drawn & Handmade |
| Pop & Print |  | Pop & Print |
| Retro & Neon |  | Retro & Neon |
| Explainers & Data |  | Explainers & Data |
| Toy, 3D & Technical |  | Toy, 3D & Technical |
| Screen & Broadcast |  | Screen & Broadcast |

Boards today, computed from the index: the story board (39 film rows) has Cartoon & Anime 20, Paper, Clay & Craft 9,
Ink & Sketch 6, Other styles 4; the explainer board (61 graphic rows) has Pop & Print 13, Explainers & Data 13,
Screen & Broadcast 11, Retro & Neon 8, Toy, 3D & Technical 7, Drawn & Handmade 9 and no Other styles.

The styles not listed here are not offered until they are proven in a rendered film.
