import tkinter as tk
import math
import time
import random
from datetime import datetime

# ─────────────────────────────────────────────────────────
#  INITIALIZE FULL SCREEN & RESOLUTION
# ─────────────────────────────────────────────────────────
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg="#00010D")

W = root.winfo_screenwidth()
H = root.winfo_screenheight()
# Shift center slightly left to give room for the sidebar
CX, CY = (W - 200) // 2, H // 2 

FPS = 60
FRAME_MS = 1000 // FPS
BG = "#00010D"

# Comprehensive Astronomical Dataset
# Scaled 'orb' values slightly to ensure Neptune (600) fits on most screens
PLANET_DATA = {
    "Mercury": {
        "orb": 70, "size": 5, "col": "#A5A5A5", "spd": 4.15, 
        "mass": "0.055 Earths", "grav": "3.7 m/s²", "dia": "4,879 km",
        "desc": "Smallest planet and closest to the Sun.",
        "fact": "A year is only 88 Earth days long!"
    },
    "Venus": {
        "orb": 110, "size": 10, "col": "#EAD4AA", "spd": 1.62, 
        "mass": "0.815 Earths", "grav": "8.87 m/s²", "dia": "12,104 km",
        "desc": "Earth's sister planet with a thick toxic atmosphere.",
        "fact": "Venus rotates backwards compared to most planets."
    },
    "Earth": {
        "orb": 155, "size": 11, "col": "#2277FF", "spd": 1.00, 
        "mass": "1.0 Earth", "grav": "9.81 m/s²", "dia": "12,742 km",
        "desc": "Our home. The only world known to harbor life.",
        "fact": "Earth is the only planet not named after a god."
    },
    "Mars": {
        "orb": 200, "size": 8, "col": "#FF4422", "spd": 0.53, 
        "mass": "0.107 Earths", "grav": "3.71 m/s²", "dia": "6,779 km",
        "desc": "The Red Planet. Home to massive dust storms.",
        "fact": "Mars has the tallest volcano in the solar system."
    },
    "Jupiter": {
        "orb": 280, "size": 25, "col": "#D3A57D", "spd": 0.15, 
        "mass": "317.8 Earths", "grav": "24.79 m/s²", "dia": "139,820 km",
        "desc": "The King of Planets. A massive gas giant.",
        "fact": "Jupiter is twice as massive as all other planets combined."
    },
    "Saturn": {
        "orb": 380, "size": 20, "col": "#F0E0A0", "spd": 0.08, 
        "mass": "95.2 Earths", "grav": "10.44 m/s²", "dia": "116,460 km",
        "desc": "Famous for its complex and beautiful ring system.",
        "fact": "Saturn is so light it would float in water."
    },
    "Uranus": {
        "orb": 480, "size": 15, "col": "#B0E0E6", "spd": 0.04, 
        "mass": "14.5 Earths", "grav": "8.69 m/s²", "dia": "50,724 km",
        "desc": "An ice giant that orbits on its side.",
        "fact": "Uranus hits the coldest temperatures of any planet."
    },
    "Neptune": {
        "orb": 580, "size": 15, "col": "#3F5EFB", "spd": 0.02, 
        "mass": "17.1 Earths", "grav": "11.15 m/s²", "dia": "49,244 km",
        "desc": "The windiest world in the entire solar system.",
        "fact": "Neptune was the first planet found by math, not sight."
    }
}

# ─────────────────────────────────────────────────────────
#  VISUAL EFFECTS CLASSES
# ─────────────────────────────────────────────────────────

class Star:
    def __init__(self):
        self.x, self.y = random.randint(0, W), random.randint(0, H)
        self.r = random.uniform(0.2, 1.8)
        self.col = random.choice(["#FFFFFF", "#D0E0FF", "#FFF0D0", "#FFD0D0"])
        self.phase = random.uniform(0, 2*math.pi)
        self.speed = random.uniform(1.2, 3.5)

class ShootingStar:
    def __init__(self):
        self.reset(); self.active = False
        self.next_spawn = time.time() + random.uniform(0.5, 4)

    def reset(self):
        self.x, self.y = random.randint(0, W // 2), random.randint(0, H // 2)
        self.len = random.randint(100, 300); self.speed = random.uniform(15, 35)
        self.opacity = 1.0; self.active = True

    def update(self):
        if not self.active:
            if time.time() > self.next_spawn: self.reset()
            return
        self.x += self.speed; self.y += self.speed * 0.35
        self.opacity -= 0.015
        if self.opacity <= 0 or self.x > W:
            self.active = False
            self.next_spawn = time.time() + random.uniform(2, 6)

def lerp_color(c1, c2, t):
    t = max(0, min(1, t))
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    return f"#{int(r1+(r2-r1)*t):02x}{int(g1+(g2-g1)*t):02x}{int(b1+(b2-b1)*t):02x}"

# ─────────────────────────────────────────────────────────
#  APP CORE
# ─────────────────────────────────────────────────────────

class GalaxyClock:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
        self.canvas.pack()

        self.stars = [Star() for _ in range(650)]
        self.shooters = [ShootingStar() for _ in range(3)]
        self.t = 0
        self.selected = None
        self.planet_pos = {}
        self.angles = {name: random.uniform(0, 6.28) for name in PLANET_DATA}
        
        self.canvas.bind("<Button-1>", self.check_click)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.loop()

    def check_click(self, event):
        for name, (px, py, r) in self.planet_pos.items():
            if math.sqrt((event.x - px)**2 + (event.y - py)**2) < r + 25:
                self.selected = name; return
        self.selected = None

    def draw(self):
        self.canvas.delete("dyn")
        self.t += 1/FPS
        
        # 1. Twinkling Stars
        for s in self.stars:
            tw = 0.2 + 0.8 * abs(math.sin(self.t * s.speed + s.phase))
            self.canvas.create_oval(s.x-s.r, s.y-s.r, s.x+s.r, s.y+s.r, fill=lerp_color(BG, s.col, tw), outline="", tags="dyn")

        # 2. Shooting Stars
        for sh in self.shooters:
            sh.update()
            if sh.active:
                x2, y2 = sh.x - sh.len, sh.y - (sh.len * 0.35)
                self.canvas.create_line(sh.x, sh.y, x2, y2, fill=lerp_color(BG, "#FFFFFF", sh.opacity), width=2, tags="dyn")

        # 3. Pulsing Sun
        s_sz = 45 + math.sin(self.t*4)*5
        self.canvas.create_oval(CX-s_sz-20, CY-s_sz-20, CX+s_sz+20, CY+s_sz+20, fill="#1F0A00", outline="", tags="dyn")
        self.canvas.create_oval(CX-s_sz, CY-s_sz, CX+s_sz, CY+s_sz, fill="#FF4500", outline="", tags="dyn")
        self.canvas.create_oval(CX-35, CY-35, CX+35, CY+35, fill="#FFD700", outline="#FFFFFF", width=2, tags="dyn")

        # 4. Planets
        for name, p in PLANET_DATA.items():
            self.angles[name] += p['spd'] * 0.006
            px = CX + p['orb'] * math.cos(self.angles[name])
            py = CY + p['orb'] * math.sin(self.angles[name])
            self.planet_pos[name] = (px, py, p['size'])

            # Orbits
            self.canvas.create_oval(CX-p['orb'], CY-p['orb'], CX+p['orb'], CY+p['orb'], outline="#0D1A30", tags="dyn")
            
            # Labels
            l_col = "#00FFFF" if self.selected == name else "#556677"
            self.canvas.create_text(px, py-p['size']-18, text=name.upper(), fill=l_col, font=("Consolas", 8, "bold"), tags="dyn")

            # Neptune & Uranus subtle glow/aura
            if name in ["Neptune", "Uranus"]:
                self.canvas.create_oval(px-p['size']-4, py-p['size']-4, px+p['size']+4, py+p['size']+4, outline=p['col'], width=1, tags="dyn")

            if name == "Saturn":
                self.canvas.create_oval(px-40, py-15, px+40, py+15, outline="#C4B484", width=2, tags="dyn")
            
            # Draw Planet
            self.canvas.create_oval(px-p['size'], py-p['size'], px+p['size'], py+p['size'], fill=p['col'], outline="#FFFFFF", tags="dyn")

        self.draw_ui()

    def draw_ui(self):
        now = datetime.now()
        # Adjusted Time/Date Bar (Centered under the Sun)
        bar_w, bar_h = 600, 80
        bx1, by1 = CX - (bar_w // 2), H - 120
        self.canvas.create_rectangle(bx1, by1, bx1+bar_w, by1+bar_h, fill="#050A1A", outline="#00AAFF", width=2, tags="dyn")
        
        # Time and Date alignment
        self.canvas.create_text(bx1 + 30, by1 + 40, text=now.strftime("%H:%M:%S"), fill="#00E5FF", font=("Consolas", 42, "bold"), anchor="w", tags="dyn")
        self.canvas.create_text(bx1 + bar_w - 30, by1 + 40, text=now.strftime("%A\n%B %d, %Y"), fill="#4488AA", font=("Consolas", 12), anchor="e", justify="right", tags="dyn")

        # Telemetry Sidebar
        if self.selected:
            d = PLANET_DATA[self.selected]
            self.canvas.create_rectangle(W-350, 50, W-50, 550, fill="#050A1A", outline=d['col'], width=3, tags="dyn")
            self.canvas.create_text(W-200, 100, text=self.selected.upper(), fill=d['col'], font=("Verdana", 26, "bold"), tags="dyn")
            
            # Physics Data
            stats = f"MASS: {d['mass']}\nGRAVITY: {d['grav']}\nDIAMETER: {d['dia']}"
            self.canvas.create_text(W-200, 180, text=stats, fill="#00FFFF", font=("Consolas", 11), justify="center", tags="dyn")
            
            self.canvas.create_text(W-200, 280, text=d['desc'], fill="white", font=("Arial", 11), width=260, justify="center", tags="dyn")
            self.canvas.create_line(W-280, 350, W-120, 350, fill="#224466", tags="dyn")
            self.canvas.create_text(W-200, 390, text="STRANGE FACT", fill="#FFCC00", font=("Arial", 10, "bold"), tags="dyn")
            self.canvas.create_text(W-200, 450, text=d['fact'], fill="#FFCC00", font=("Arial", 11, "italic"), width=260, justify="center", tags="dyn")

    def loop(self):
        self.draw()
        self.root.after(FRAME_MS, self.loop)

if __name__ == "__main__":
    app = GalaxyClock(root)
    root.mainloop()
    