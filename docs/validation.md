# Prism Hop upgrade validation

## Board and camera

Every route is now a larger prism field: the opening route has **8 rows / 36 tiles**, and the finale has **11 rows / 66 tiles**. The prior game ranged from 4 rows / 10 tiles to 7 rows / 28 tiles. Prism Hop now uses a 230×149 gameplay viewport over a smaller-scale world coordinate system. The camera follows the hopper toward the center and clamps to the prism-field bounds at the apex and edges.

`test-core.js` checks triangular topology, route counts, enemy paths, enlarged board sizes, camera bounds, and that the camera position changes between the apex and final prism.

## Tilt tuning

The R1 bridge integration uses the documented `window.creationSensors.accelerometer` hook at 30 Hz. A new run gathers five valid samples to establish the neutral position. Subsequent samples are offset from neutral, exponentially smoothed (38% new sample), require a 0.16 dead zone, and need 12% axis dominance before producing one of the four diagonal hop directions. A reading expires after 420 ms. Route hop repeat is 244–330 ms, allowing a deliberate held tilt to repeat without creating a noisy move from minor device motion.

Browser testing injects neutral and tilted samples to validate the calibration, dead zone/smoothing path, direction mapping, and repeat path. This does **not** confirm R1 sensor polarity, ergonomics, latency, or physical responsiveness.

## Artwork and touch fallback

The visual upgrade combines compact generated project artwork with lightweight canvas drawing. `assets/prism-atmosphere.webp` is original floating-crystal atmosphere art generated for Prism Hop on 2026-10-31, downscaled to a 360×420 menu background. `assets/board-dawn.webp` and `assets/board-storm.webp` are original 240×149 color-derived board plates. They are composited under six palette-scripted route themes; tiles, runes, hopper, crawler, unstable cracks, Phase ring, and hop/collision bursts are drawn in Canvas at runtime. No Q*bert art, layouts, or branding is included.

There is no visible movement pad. During an active run, an invisible 230×149 gesture plane lies exactly over the board: dragging away from the hopper into a diagonal chooses the hop direction. A short double tap inside that field activates Phase Ring; wheel up remains a hardware alternative. The browser suite exercises drag and double-tap events. This is a fallback for unavailable/unpermitted motion; it does not replace tilt-first R1 play.

## Audio

All sound is original procedural Web Audio. The game lazy-creates its audio context during gameplay actions, resumes a suspended context where the browser permits it, and exposes a visible speaker control. Hop, menu, start, Phase Ring, collision, and route-clear cues use short oscillator envelopes; the mute state suppresses every cue. The state is retained locally when available. Browser validation checks the control and page flow; output volume and audio latency still need a physical R1 check.

## Browser validation

Run the following from the project directory:

```sh
node --check game-core.js && node --check app.js
node test-core.js
python3 -m http.server 8765 --directory .
# in a second terminal
python3 test-browser.py
```

The browser suite uses a 240×282 touch viewport and checks menu, expanded gameplay, simulated motion calibration/hop, drag direction, double-tap Phase, pause/resume, results, page overflow, and Chromium frame pacing. The screenshots under `test-results/` are browser captures, not photos from an R1; Chromium pacing does not establish physical R1 frame rate.
