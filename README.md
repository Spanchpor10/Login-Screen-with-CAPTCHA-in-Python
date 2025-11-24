<div align="center">

# 🎫 Professional Login System
### Tkinter GUI + Custom CAPTCHA Generator


</div>

---

## ⭐ Overview

This project demonstrates a production-feeling login system built entirely in Python. Unlike standard Tkinter demos, this project implements a **custom security engine** that generates CAPTCHAs from scratch using `Pillow`, complete with noise, jitter, and rotation, mimicking server-side authentication logic on a local client.

**Key Highlights:**
* **Modern UI:** Clean layout with company branding and responsive-feeling inputs.
* **Dynamic Security:** Real-time image generation (no static assets).
* **Session Logic:** TTL (Time-to-Live) enforcement for CAPTCHAs.

---

## 🚩 Key Features

| Feature | Description |
| :--- | :--- |
| **🔒 Robust CAPTCHA** | Generates unique images with line noise, dot noise, and rotation filters. |
| **⏳ Time-Sensitive** | Implements a "TTL" (Time To Live) check; CAPTCHAs expire after 120 seconds. |
| **👁️ Anti-Bot Visuals** | Uses per-character jitter and smoothing/sharpening filters to resist OCR. |
| **🔁 Smart UX** | Auto-refresh on failure, manual refresh button, and helpful error messages. |
| **📦 Zero-Bloat** | Entire application logic contained in a single Python script. |

---

## 💻 Quick Start

### Prerequisites
* Python 3.8+
* `pip`

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Spanchpor10/Login-Screen-with-CAPTCHA-in-Python.git](https://github.com/Spanchpor10/Login-Screen-with-CAPTCHA-in-Python.git)
    cd professional-login-captcha
    ```

2.  **Set up a virtual environment (Recommended)**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install Pillow
    ```

4.  **Run the App**
    ```bash
    python professional_login_captcha.py
    ```

### 🔑 Demo Credentials
Use these credentials to test the successful login flow:
> **Username:** `admin`
> **Password:** `Password123`

---

## 🔧 Technical Architecture

### How the CAPTCHA is Generated
The `CaptchaGenerator` class utilizes `Pillow` (PIL) to create images on the fly. The process ensures a balance between human readability and bot resistance:

1.  **Text Generation:** Selects random alphanumeric characters (excluding ambiguous ones like `0`, `O`, `1`, `I`).
2.  **Canvas Creation:** Creates an RGBA canvas.
3.  **Character Rendering:**
    * Each character is drawn on a temporary layer.
    * **Rotation:** Randomly rotated ±`CHAR_ROTATION_MAX` degrees.
    * **Jitter:** Random X/Y offset applied to break alignment.
4.  **Noise Injection:**
    * **Lines:** Draws random lines across the text.
    * **Dots:** Sprinkles noise pixels to confuse segmentation algorithms.
5.  **Post-Processing:** Applies `SMOOTH` and `SHARPEN` filters for blending.

### Verification Logic
The system mimics a server-side session store:
* **Hashing:** Passwords in the demo store are SHA-256 hashed.
* **Single-Use:** Once a CAPTCHA is verified (pass or fail), it is invalidated to prevent replay attacks.
* **Case-Insensitivity:** CAPTCHA input is normalized before comparison.

---

## ⚙️ Configuration

You can tune the application behavior by modifying the constants at the top of `professional_login_captcha.py`:

| Constant | Default | Purpose |
| :--- | :--- | :--- |
| `CAPTCHA_LENGTH` | `5` | Number of characters in the image. |
| `CAPTCHA_TTL_SECONDS` | `120` | How long a CAPTCHA remains valid. |
| `LINE_NOISE` | `6` | Intensity of interference lines. |
| `CHAR_ROTATION_MAX` | `25` | Max rotation degrees per character. |
| `COMPANY_NAME` | `...` | Text displayed in the UI header. |

---

## 🔐 Security Note

> [!WARNING]
> **This is a portfolio demonstration.**
> While this project implements secure *concepts* (hashing, salts, TTL), it runs entirely on the client-side.
> * **Do not** use this exact code for a production app handling sensitive data.
> * In production, CAPTCHA generation and verification must happen on a **backend server**.

---

## 🧪 Future Improvements

This project is designed to be extended. Here are planned features:

- [ ] Replace demo auth with **SQLite + SQLAlchemy**.
- [ ] Integrate **bcrypt** for industry-standard password hashing.
- [ ] Separate the CAPTCHA engine into a **Flask/FastAPI microservice**.
- [ ] Add **GitHub Actions** for automated linting and testing.
- [ ] Package as a `.exe` using **PyInstaller**.

---

## 👤 Author

**Sarthak Panchpor**
* Student at PVG’s COET, Pune
* Passionate about Python, GUI Development, and System Design.

---

<div align="center">
  <sub>Built with ❤️ using Python and Tkinter</sub>
</div>
