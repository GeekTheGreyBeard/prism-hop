# Prism Hop

**Prism Hop** is an original, compact arcade game for the rabbit r1. Guide a bright hopper across an isometric prism array, tune every tile, evade Static Crawlers, and use a short Phase Ring at the right moment.

![Prism Hop menu at 240×282](./test-results/menu-240x282.png)

## Play

- **Goal:** tune every prism tile in the current route. A tuned tile stays cyan.
- **Movement:** on an r1, tilt the device to choose one of four diagonal hops. A sustained tilt triggers one hop at the route's tempo.
- **Wheel:** on the menu, scroll up/down to choose an unlocked route. During play, **wheel up** activates the three-second **Phase Ring** (seven-second recharge), which protects the hopper and displaces crawlers.
- **Side button:** start a route from the menu; pause or resume a route during play.
- **Accessible fallback:** large on-screen direction pads always work. In a browser, keys **1–4** simulate diagonal hops, **Up Arrow** triggers Phase Ring, **Space** performs the side-button action, and mouse-wheel simulates r1 wheel events.
- **Hazards:** leaving the pyramid, landing on a magenta unstable prism without Phase Ring, or touching a Static Crawler costs one of three lives.

## Routes

Six original routes escalate from four to seven rows, introduce more crawlers and unstable prisms, and reduce the time between hops: **Dawn Array**, **Mirror Steps**, **Signal Bloom**, **Night Relay**, **Prism Storm**, and **Aurora Apex**. Progress unlocks locally in browser storage or the r1 creation storage fallback.

## R1 integration and limits

The game guards access to `window.creationSensors.accelerometer`: it starts only if the R1 bridge reports an available accelerometer and uses samples at 30 Hz. The page listens for the documented `scrollUp`, `scrollDown`, and `sideClick` bridge events. It does **not** claim that wheel direction, accelerometer polarity, frame rate, touch ergonomics, or audio have been validated on physical R1 hardware; browser simulation only validates the page’s input logic.

## Sound and assets

All art is procedural HTML/CSS/SVG created for this project. Sound effects are short Web Audio oscillator cues generated at runtime. There are no copied arcade assets, external artwork, samples, fonts, or third-party runtime dependencies.

## Testing

```sh
node --check game-core.js && node --check app.js
node test-core.js
python3 -m http.server 8765
```

The project was reviewed at a 240×282 browser viewport with no page scroll. The menu, gameplay board, controls, pause, result overlay, touch fallback, and missing-sensor fallback should be checked in a browser before release. Browser injected motion/wheel events are simulations, not physical R1 verification.

## Install on R1

The installation QR below encodes the Rabbit Creations SDK metadata card in [`creation-card.json`](./creation-card.json). Open **Creations → Create → Add via QR code** on an r1 and scan it from another screen.

![Installation QR](./prism-hop-install.png)

Published game: _added after Pages deployment_.
