#!/usr/bin/env python3
"""
Thumbnail system for @irfanismailm
Tokens lifted verbatim from irfanismailm.com/styles.css
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

F = "/home/claude/fonts"
OUT = "/mnt/user-data/outputs/thumbnails"

# ---- brand tokens (styles.css :root) ----
PAPER = (250, 246, 239)
TILE  = (255, 253, 248)
INK   = (33, 31, 40)
SOFT  = (110, 104, 120)
DIM   = (154, 148, 160)
HAIR  = (231, 224, 212)
CORAL = (255, 90, 60)
INDIGO= (76, 91, 255)
EMER  = (20, 179, 125)
VIOLET= (139, 61, 255)
AMBER = (255, 176, 32)

S = 2  # supersample

def font(name, size):
    return ImageFont.truetype(f"{F}/{name}.ttf", int(size * S))

def px(v): return int(round(v * S))

# ---------- background: paper + the two radial washes from body::before ----------
def background(W, H):
    w, h = W * S, H * S
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    x /= w; y /= h
    base = np.zeros((h, w, 3), np.float32)
    base[:] = PAPER

    def wash(cx, cy, rx, ry, color, alpha, stop):
        d = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
        a = np.clip(1.0 - d / stop, 0, 1) ** 1.6 * alpha
        for i in range(3):
            base[:, :, i] = base[:, :, i] * (1 - a) + color[i] * a

    wash(0.50, -0.08, 0.90, 0.60, CORAL, 0.07, 1.0)   # radial-gradient(90% 60% at 50% -8%)
    wash(1.00,  0.00, 0.70, 0.50, INDIGO, 0.05, 1.0)  # radial-gradient(70% 50% at 100% 0%)
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")

# ---------- letter-spaced text (Pillow has no tracking) ----------
def tracked_width(text, fnt, track_px):
    return sum(fnt.getlength(c) for c in text) + track_px * S * max(0, len(text) - 1)

def draw_tracked(d, xy, text, fnt, fill, track_px=0):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill)
        x += fnt.getlength(c) + track_px * S

# ---------- the coral signature stroke (.sigstroke path { fill: var(--coral) }) ----------
def swash(d, x0, x1, y, thick):
    """Tapered marker underline, thin at the ends, lifting slightly to the right."""
    x0, x1, y, t = x0 * S, x1 * S, y * S, thick * S
    pts_top, pts_bot = [], []
    n = 64
    for i in range(n + 1):
        u = i / n
        cy = y - 3 * S * math.sin(u * math.pi) - 5 * S * u          # gentle arc + rise
        taper = math.sin(min(1.0, u * 1.15) * math.pi) ** 0.55       # thin at both ends
        half = t * (0.16 + 0.84 * taper) / 2
        px_ = x0 + (x1 - x0) * u
        pts_top.append((px_, cy - half))
        pts_bot.append((px_, cy + half))
    d.polygon(pts_top + pts_bot[::-1], fill=CORAL)

# ---------- title fitting ----------
def fit_title(text, max_w, max_size, min_size, track_em=-0.03):
    for size in range(int(max_size), int(min_size) - 1, -2):
        fnt = font("bric700", size)
        tr = track_em * size
        words, lines, cur = text.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if tracked_width(trial, fnt, tr) <= max_w * S or not cur:
                cur = trial
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) <= 2 and all(tracked_width(l, fnt, tr) <= max_w * S for l in lines):
            return fnt, tr, lines, size
    return fnt, tr, lines, size

# ---------- one thumbnail ----------
def thumb(W, H, eyebrow, title, meta, accent, path):
    img = background(W, H).convert("RGBA")
    d = ImageDraw.Draw(img)

    # corner crop marks (.cropmarks)
    m, inset, sw = 26, 34, 2
    for cx, cy, dx, dy in ((inset, inset, 1, 1), (W - inset, inset, -1, 1),
                           (inset, H - inset, 1, -1), (W - inset, H - inset, -1, -1)):
        d.line([(px(cx), px(cy)), (px(cx + dx * m), px(cy))], fill=HAIR, width=px(sw))
        d.line([(px(cx), px(cy)), (px(cx), px(cy + dy * m))], fill=HAIR, width=px(sw))

    # card (.lane: tile fill, hair border, 16px radius, 3px accent bar on top)
    pad = round(W * 0.062)
    top, bot = round(H * 0.115), H - round(H * 0.115)
    r = px(20)
    box = [px(pad), px(top), px(W - pad), px(bot)]
    d.rounded_rectangle(box, radius=r, fill=TILE, outline=HAIR, width=px(1.5))

    bar = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(bar).rectangle([box[0], box[1], box[2], box[1] + px(4)], fill=accent)
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=r, fill=255)
    img.paste(bar, (0, 0), Image.composite(mask, Image.new("L", img.size, 0), mask))
    d = ImageDraw.Draw(img)

    cx0 = pad + round(W * 0.052)
    cx1 = W - pad - round(W * 0.052)
    inner_w = cx1 - cx0

    # eyebrow: Space Mono, uppercase, .2em tracking, accent (.eyebrow)
    eb_size = max(11, round(W * 0.0155))
    eb = font("mono700", eb_size)
    y = top + round(H * 0.115)
    draw_tracked(d, (px(cx0), px(y)), eyebrow.upper(), eb, accent, eb_size * 0.20)

    # title: Bricolage Grotesque 700, -.03em (.section-title / .handle-big)
    fnt, tr, lines, tsize = fit_title(title, inner_w, W * 0.082, W * 0.036)
    ty = y + round(H * 0.085)
    lh = tsize * 1.03
    for i, line in enumerate(lines):
        draw_tracked(d, (px(cx0), px(ty + i * lh)), line, fnt, INK, tr)

    # coral stroke under the final word (.sigstroke)
    last = lines[-1]
    word = last.split()[-1] if last.split() else last
    pre = last[: len(last) - len(word)]
    wx0 = cx0 + tracked_width(pre, fnt, tr) / S
    wx1 = wx0 + tracked_width(word, fnt, tr) / S
    last_top = ty + (len(lines) - 1) * lh
    glyph_bottom = fnt.getbbox(word)[3] / S          # clears descenders (p, g, y)
    base_y = last_top + max(glyph_bottom, tsize * 0.88) + tsize * 0.075
    swash(d, wx0, wx1, base_y, tsize * 0.135)

    # hairline + footer (.hr / footer mono)
    fy = bot - round(H * 0.135)
    d.line([(px(cx0), px(fy)), (px(cx1), px(fy))], fill=HAIR, width=px(1.5))

    f_size = max(10, round(W * 0.0145))
    fm = font("mono400", f_size)
    handle_y = fy + round(H * 0.048)
    draw_tracked(d, (px(cx0), px(handle_y)), "@irfanismailm", fm, SOFT, f_size * 0.06)

    mtxt = meta.upper()
    mw = tracked_width(mtxt, fm, f_size * 0.14) / S
    dot = px(f_size * 0.30)
    d.ellipse([px(cx1 - mw - f_size * 1.15), px(handle_y + f_size * 0.42),
               px(cx1 - mw - f_size * 1.15) + dot, px(handle_y + f_size * 0.42) + dot], fill=accent)
    draw_tracked(d, (px(cx1 - mw), px(handle_y)), mtxt, fm, DIM, f_size * 0.14)

    img.convert("RGB").resize((W, H), Image.LANCZOS).save(path, quality=96, optimize=True)
    return path


PROJECTS = [
    ("Showreel · 2026",        "Recent Works Compilation", "2026", CORAL,  "recent-works-compilation"),
    ("CGI · Real Estate",      "CGI Reel for Real Estate", "2025", INDIGO, "cgi-reel-real-estate"),
    ("VFX Breakdown",          "Eid CGI Reel",             "2025", VIOLET, "eid-cgi-reel-vfx"),
    ("2D Motion · Podcast",    "Podcast Visual Reel",      "2025", EMER,   "podcast-visual-reel"),
    ("Motion Design · 2023",   "2023 Motion Designs",      "2023", CORAL,  "2023-motion-designs"),
    ("3D Motion · Product",    "Swiss Army Knife",         "2023", INDIGO, "swiss-army-knife"),
    ("Brand Reveal",           "Malak Brand Reveal",       "2022", VIOLET, "malak-brand-reveal"),
    ("3D Loop · Ad",           "Halloween 3D Loop Ad",     "2023", AMBER,  "halloween-3d-loop"),
    ("3D Motion · Ad",         "3D Motion Ad",             "2023", AMBER,  "3d-motion-ad"),
    ("3D Visualization",       "Exhibition Stall",         "2023", INDIGO, "exhibition-stall"),
]

SIZES = {"vimeo-1280x720": (1280, 720), "behance-808x632": (808, 632)}

made = {}
for folder, (W, H) in SIZES.items():
    os.makedirs(f"{OUT}/{folder}", exist_ok=True)
    made[folder] = []
    for eb, title, meta, accent, slug in PROJECTS:
        p = f"{OUT}/{folder}/{slug}.png"
        thumb(W, H, eb, title, meta, accent, p)
        made[folder].append(p)

# contact sheet of the 16:9 set
cols, cw, ch, gap = 2, 640, 360, 24
rows = math.ceil(len(PROJECTS) / cols)
sheet = Image.new("RGB", (cols * cw + (cols + 1) * gap, rows * ch + (rows + 1) * gap), PAPER)
for i, p in enumerate(made["vimeo-1280x720"]):
    im = Image.open(p).resize((cw, ch), Image.LANCZOS)
    sheet.paste(im, (gap + (i % cols) * (cw + gap), gap + (i // cols) * (ch + gap)))
sheet.save(f"{OUT}/00-contact-sheet.png", quality=95, optimize=True)
print("done", sum(len(v) for v in made.values()), "files")
