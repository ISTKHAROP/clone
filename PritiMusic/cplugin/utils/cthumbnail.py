import os
import re
import random
import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from py_yt import VideosSearch
from PritiMusic import app
from PritiMusic.utils.database import clonebotdb


# =========================
# 🔥 Circular Glow Helper
# =========================
def get_glowing_circle(image_path, size=(500, 500), glow_radius=25):

    img = Image.open(image_path).convert("RGBA")
    img = img.resize(size)

    # circular mask
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    # apply circle crop
    circle = img.copy()
    circle.putalpha(mask)

    # glow layer
    glow = circle.filter(ImageFilter.GaussianBlur(glow_radius))

    # brighten glow
    enhancer = ImageEnhance.Brightness(glow)
    glow = enhancer.enhance(1.4)

    # base canvas
    base = Image.new("RGBA", size, (0, 0, 0, 255))

    # merge glow + image
    base = Image.alpha_composite(base, glow)
    base = Image.alpha_composite(base, circle)

    return base


# =========================
# 🎵 Clean Lyrics Drawer (NO CHAPRI COLORS)
# =========================
def draw_lyrics(image, text, font_path=None):

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path or "arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    # soft white only (clean style)
    shadow_color = (0, 0, 0, 160)
    text_color = (255, 255, 255, 230)

    x, y = 30, image.size[1] - 120

    # shadow
    draw.text((x+2, y+2), text, font=font, fill=shadow_color)

    # main text
    draw.text((x, y), text, font=font, fill=text_color)

    return image


# =========================
# 🎧 MAIN FUNCTION EXAMPLE
# =========================
async def create_song_image(image_path, lyrics):

    base = get_glowing_circle(image_path)

    final = draw_lyrics(base, lyrics)

    out = "output.png"
    final.save(out)

    return out
