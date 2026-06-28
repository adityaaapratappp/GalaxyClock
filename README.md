# 🌌 Galaxy Clock

A fullscreen, animated solar system clock built with Python and Tkinter. Watch all 8 planets orbit the Sun in real time while a live clock ticks in the corner — click any planet to pull up its stats and a fun space fact.

![Python](https://img.shields.io/badge/Python-3.8+-00E5FF?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-3F5EFB?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-FFD700?style=for-the-badge)

---

## ✨ Features

- **Live Planetary Orbits** — All 8 planets orbit at scaled relative speeds
- **Twinkling Starfield** — 650 stars with randomized twinkle animations
- **Shooting Stars** — Random shooting stars streak across the background
- **Pulsing Sun** — Animated glowing Sun at the center
- **Saturn's Rings** — Visually rendered ring system
- **Live Clock** — Real-time HH:MM:SS display with date
- **Planet Telemetry** — Click any planet to see mass, gravity, diameter, description & a fun fact
- **Fullscreen** — Runs edge-to-edge; press `Esc` to exit

---

## 🪐 Planets Included

| Planet | Color | Fun Fact |
|--------|-------|----------|
| Mercury | Gray | A year is only 88 Earth days long! |
| Venus | Pale Gold | Rotates backwards compared to most planets |
| Earth | Blue | Only planet not named after a god |
| Mars | Red | Home to the tallest volcano in the solar system |
| Jupiter | Tan | Twice as massive as all other planets combined |
| Saturn | Yellow | So light it would float in water |
| Uranus | Ice Blue | Hits the coldest temperatures of any planet |
| Neptune | Deep Blue | First planet found by math, not sight |

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/adityaaapratappp/Galaxy-Clock.git
cd Galaxy-Clock
```

### 2. Install dependencies

Tkinter comes pre-installed with Python. No extra packages needed!

> If Tkinter is missing on Linux: `sudo apt install python3-tk`

### 3. Run the app

```bash
python galaxy_clock.py
```

> **Note:** Runs best on a large/fullscreen display. Press `Esc` to quit.

---

## 🖥️ Usage

- Launch the app — the solar system starts animating immediately
- **Click any planet** to open its telemetry panel on the right
- **Click empty space** to close the panel
- Press **Esc** to exit fullscreen

---

## ⚙️ Customization

Planet speeds, sizes, colors, and data are all in the `PLANET_DATA` dictionary at the top of the file — easy to tweak:

```python
"Earth": {
    "orb": 155,       # Orbit radius in pixels
    "size": 11,       # Planet radius in pixels
    "col": "#2277FF", # Color
    "spd": 1.00,      # Relative orbital speed
    ...
}
```

To add more stars or shooting stars, change these lines:

```python
self.stars = [Star() for _ in range(650)]      # Increase for denser starfield
self.shooters = [ShootingStar() for _ in range(3)]  # Increase for more shooting stars
```

---

## 🤖 AI Assistance

This project was independently developed by [@adityaaapratappp](https://github.com/adityaaapratappp). **[Claude](https://claude.ai)** by Anthropic was consulted solely in areas where specific technical knowledge was required — such as animation logic and canvas rendering — and was not involved in the project concept, design direction, or overall structure.

---

## 👤 Author

Made by [@adityaaapratappp](https://github.com/adityaaapratappp)

---
## 📄 License

MIT License — feel free to fork, modify, and explore the cosmos with it.
