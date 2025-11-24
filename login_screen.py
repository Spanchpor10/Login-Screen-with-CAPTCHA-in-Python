#!/usr/bin/env python3
"""
professional_login_captcha.py

Polished login screen (Tkinter) with integrated CAPTCHA verification.
Single-file demo: change the demo user/password & integrate with a real DB when needed.

Requirements:
    pip install Pillow

Run:
    python professional_login_captcha.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageTk
import random, string, io, time, hashlib

# -----------------------
# Configuration
# -----------------------
APP_TITLE = "Acme Corp — Secure Login"
COMPANY_NAME = "ACME CORPORATION"
LOGO_PLACEHOLDER_TEXT = "LOGO"
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 360

# CAPTCHA config
CAPTCHA_LENGTH = 5
CAPTCHA_WIDTH = 260
CAPTCHA_HEIGHT = 90
CAPTCHA_FONT_SIZE = 36
LINE_NOISE = 5
DOT_NOISE = 120
CHAR_ROTATION_MAX = 25
CAPTCHA_TTL_SECONDS = 120  # seconds before captcha expires

# Demo user (replace with DB-backed auth in real apps)
# password stored as SHA-256 hash of "Password123"
DEMO_USERS = {
    "admin": hashlib.sha256("Password123".encode("utf-8")).hexdigest(),
    "user": hashlib.sha256("qwertyUIOP1".encode("utf-8")).hexdigest()
}

# Allowed characters for captcha (avoid ambiguous ones)
ALLOWED_CHARS = ''.join(ch for ch in (string.ascii_uppercase + string.digits) if ch not in "0O1IJL")

# -----------------------
# Helper: CAPTCHA generation
# -----------------------
def _random_color(minv=0, maxv=160):
    return tuple(random.randint(minv, maxv) for _ in range(3))

def _load_font(size=CAPTCHA_FONT_SIZE):
    # Attempt to load common TTF fonts; fallback to default.
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()

def generate_captcha_text(length=CAPTCHA_LENGTH):
    return ''.join(random.choice(ALLOWED_CHARS) for _ in range(length))

def render_captcha_image(text,
                         width=CAPTCHA_WIDTH,
                         height=CAPTCHA_HEIGHT,
                         font_size=CAPTCHA_FONT_SIZE,
                         line_noise=LINE_NOISE,
                         dot_noise=DOT_NOISE):
    font = _load_font(font_size)
    image = Image.new("RGB", (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(image)

    # noise lines
    for _ in range(line_noise):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=_random_color(60, 200), width=random.randint(1, 3))

    # compute text bounding and starting coordinates
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2

    # draw characters separately with rotation/jitter
    for ch in text:
        ch_bbox = draw.textbbox((0, 0), ch, font=font)
        ch_w = ch_bbox[2] - ch_bbox[0]
        ch_h = ch_bbox[3] - ch_bbox[1]

        char_img = Image.new("RGBA", (ch_w * 3, ch_h * 3), (0, 0, 0, 0))
        cd = ImageDraw.Draw(char_img)
        cd.text((ch_w, ch_h // 2), ch, font=font, fill=_random_color(20, 220))

        angle = random.uniform(-CHAR_ROTATION_MAX, CHAR_ROTATION_MAX)
        rotated = char_img.rotate(angle, resample=Image.BILINEAR, expand=1)

        y_jitter = y + random.randint(-6, 6)
        image.paste(rotated, (x + random.randint(-2, 2), y_jitter), rotated)
        x += ch_w

    # dot noise
    for _ in range(dot_noise):
        draw.point((random.randint(0, width - 1), random.randint(0, height - 1)),
                   fill=_random_color(0, 200))

    # slight blur/sharpen to blend
    image = image.filter(ImageFilter.SMOOTH).filter(ImageFilter.SHARPEN)
    return image

def pil_to_tk(img):
    return ImageTk.PhotoImage(img)

# -----------------------
# Captcha session (in-memory)
# -----------------------
class CaptchaSession:
    def __init__(self):
        self.text = None
        self.image = None
        self.created_at = None

    def create(self):
        self.text = generate_captcha_text()
        self.image = render_captcha_image(self.text)
        self.created_at = time.time()

    def is_valid(self):
        if not self.text or not self.created_at:
            return False
        return (time.time() - self.created_at) <= CAPTCHA_TTL_SECONDS

    def verify(self, attempt):
        if not self.is_valid():
            return False, "expired"
        if attempt.strip().upper() == self.text.upper():
            return True, "ok"
        return False, "incorrect"

# -----------------------
# Main Tkinter UI
# -----------------------
class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._setup_styles()

        self.captcha = CaptchaSession()
        self._build_ui()
        self._new_captcha()

    def _setup_styles(self):
        # Basic, clean styles
        self.style.configure("Card.TFrame", background="#ffffff", relief="flat")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="#f4f6f9")
        self.style.configure("Title.TLabel", font=("Helvetica", 18, "bold"))
        self.style.configure("Sub.TLabel", font=("Segoe UI", 10))
        self.style.configure("TButton", padding=6)
        self.style.configure("Accent.TButton", background="#0b63d6", foreground="white")

    def _build_ui(self):
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        # Top band with company name and placeholder logo
        top = ttk.Frame(root, height=70)
        top.pack(fill="x", pady=(0, 8))

        logo_frame = ttk.Frame(top, width=140, height=70)
        logo_frame.pack(side="left", padx=(0, 12))
        logo_frame.pack_propagate(False)
        logo_canvas = tk.Canvas(logo_frame, width=120, height=60, bg="#ffffff", highlightthickness=0)
        logo_canvas.pack()
        # draw placeholder "logo" rectangle & text
        logo_canvas.create_rectangle(4, 4, 116, 56, outline="#d0d7de", width=1, fill="#f6f8fa")
        logo_canvas.create_text(60, 30, text=LOGO_PLACEHOLDER_TEXT, fill="#5a6b7a", font=("Segoe UI", 10, "bold"))

        title_frame = ttk.Frame(top)
        title_frame.pack(side="left", anchor="center")
        ttk.Label(title_frame, text=COMPANY_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_frame, text="Secure sign-in portal", style="Sub.TLabel").pack(anchor="w")

        # Card container
        card = ttk.Frame(root, style="Card.TFrame", padding=14, relief="groove")
        card.pack(fill="both", expand=True)

        # Username/password area
        form = ttk.Frame(card)
        form.pack(side="left", padx=(0, 12), pady=4, fill="y")

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w")
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(form, textvariable=self.username_var, width=28)
        self.username_entry.grid(row=1, column=0, pady=(0, 8))

        ttk.Label(form, text="Password").grid(row=2, column=0, sticky="w")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(form, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=3, column=0, pady=(0, 8))

        self.remember_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(form, text="Remember me", variable=self.remember_var).grid(row=4, column=0, sticky="w", pady=(0, 8))

        # CAPTCHA & buttons area
        right = ttk.Frame(card)
        right.pack(side="left", fill="both", expand=True)

        # captcha image canvas
        self.captcha_canvas = tk.Canvas(right, width=CAPTCHA_WIDTH, height=CAPTCHA_HEIGHT, bg="#f0f0f0", highlightthickness=0)
        self.captcha_canvas.pack(anchor="e", pady=(0,6))

        # captcha input
        ttk.Label(right, text="Enter CAPTCHA").pack(anchor="w")
        self.captcha_var = tk.StringVar()
        self.captcha_entry = ttk.Entry(right, textvariable=self.captcha_var)
        self.captcha_entry.pack(fill="x", pady=(4, 6))

        btns = ttk.Frame(right)
        btns.pack(fill="x", pady=(6, 0))
        ttk.Button(btns, text="Refresh CAPTCHA", command=self._new_captcha).pack(side="left")
        ttk.Button(btns, text="Use Demo (autofill)", command=self._autofill_demo).pack(side="left", padx=(8,0))
        ttk.Button(btns, text="Login", command=self._on_login).pack(side="right")

        # status message
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status_var, foreground="#333").pack(anchor="w", pady=(8,0))

        # keyboard bindings
        self.bind("<Return>", lambda e: self._on_login())

    def _render_captcha_on_canvas(self):
        # convert PIL -> PhotoImage
        tkimg = pil_to_tk(self.captcha.image)
        self._current_captcha_img = tkimg  # keep reference
        self.captcha_canvas.config(width=tkimg.width(), height=tkimg.height())
        self.captcha_canvas.delete("all")
        self.captcha_canvas.create_image(0, 0, anchor="nw", image=tkimg)

    def _new_captcha(self):
        self.captcha.create()
        self._render_captcha_on_canvas()
        self.captcha_var.set("")
        self.status_var.set("CAPTCHA refreshed")

    def _autofill_demo(self):
        # Demo helper: autofill correct captcha (for demo/testing)
        if self.captcha.text:
            self.captcha_var.set(self.captcha.text)
            self.status_var.set("Demo: captcha autofilled (for testing)")

    def _on_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        captcha_attempt = self.captcha_var.get().strip()

        # form validation
        if not username or not password:
            messagebox.showwarning("Missing fields", "Please enter both username and password.")
            return

        # verify captcha first
        ok, reason = self.captcha.verify(captcha_attempt)
        if not ok:
            if reason == "expired":
                messagebox.showwarning("CAPTCHA expired", "CAPTCHA expired. A new one will be generated.")
                self._new_captcha()
                return
            else:
                messagebox.showerror("CAPTCHA invalid", "CAPTCHA incorrect. Try again.")
                # optional: refresh on repeated failures; here we just notify
                self._new_captcha()
                return

        # verify credentials (demo: SHA-256)
        pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        stored_hash = DEMO_USERS.get(username)
        if stored_hash and stored_hash == pwd_hash:
            # login success
            self.status_var.set(f"Welcome, {username} — logged in successfully.")
            messagebox.showinfo("Login successful", f"Welcome, {username}!")
            # Invalidate used captcha and optionally proceed to next screen
            self.captcha.text = None
            # optionally clear password field
            self.password_var.set("")
            # Here you'd switch to the app main window or perform token exchange, etc.
        else:
            messagebox.showerror("Login failed", "Invalid username or password.")
            self.status_var.set("Login failed")
            # refresh captcha to prevent brute-force attempts
            self._new_captcha()

# -----------------------
# Run
# -----------------------
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
