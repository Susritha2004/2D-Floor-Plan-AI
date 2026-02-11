from PIL import Image, ImageDraw

# =========================
# HELPERS
# =========================

def draw_label(draw, x, y, text):
    draw.rectangle([x-2, y-2, x+230, y+18], fill="white")
    draw.text((x, y), text, fill="black")

def draw_door(draw, x, y, orientation):
    if orientation == "right":
        draw.arc([x-20, y-20, x+20, y+20], 270, 360, fill="black", width=2)
    elif orientation == "left":
        draw.arc([x-20, y-20, x+20, y+20], 90, 180, fill="black", width=2)
    elif orientation == "down":
        draw.arc([x-20, y-20, x+20, y+20], 0, 90, fill="black", width=2)

def draw_window(draw, x1, y1, x2, y2):
    draw.line([x1, y1, x2, y2], fill="skyblue", width=4)

def clamp(rect, margin, pw, ph):
    rect["x"] = max(margin+5, min(rect["x"], margin+pw-rect["w"]-5))
    rect["y"] = max(margin+5, min(rect["y"], margin+ph-rect["h"]-5))
    return rect

def overlaps(a, b):
    return not (
        a["x"] + a["w"] <= b["x"] or
        a["x"] >= b["x"] + b["w"] or
        a["y"] + a["h"] <= b["y"] or
        a["y"] >= b["y"] + b["h"]
    )

def auto_place(rect, placed, max_x, max_y, step=20):
    while True:
        collision = False
        for r in placed:
            if overlaps(rect, r):
                collision = True
                rect["y"] += step
                if rect["y"] + rect["h"] > max_y:
                    rect["y"] = 80
                    rect["x"] += step
                break
        if not collision:
            return rect

# =========================
# MAIN DRAW FUNCTION
# =========================

def draw_floorplan(data, output_path="static/floorplan.png"):
    scale = 10
    margin = 60

    plot_w, plot_h = data["plot_size"]
    pw, ph = plot_w * scale, plot_h * scale

    canvas_w = pw + margin*2 + 120
    canvas_h = ph + margin*2 + 120

    img = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(img)

    # Plot boundary
    draw.rectangle([margin, margin, margin+pw, margin+ph], outline="black", width=3)
    draw.text((margin, margin-25), f"{plot_w} x {plot_h} ft Plot", fill="black")

    placed = []
    bedroom_positions = []

    # =========================
    # BEDROOMS (WEST)
    # =========================
    bx, by = margin+20, margin+80

    for i, bed in enumerate(data["bedrooms"]):
        bw, bh = bed["width"]*scale, bed["height"]*scale

        rect = {"x": bx, "y": by, "w": bw, "h": bh}
        rect = auto_place(rect, placed, margin+pw*0.45, margin+ph)
        rect = clamp(rect, margin, pw, ph)
        placed.append(rect)

        draw.rectangle([rect["x"], rect["y"], rect["x"]+bw, rect["y"]+bh],
                       outline="blue", width=3)
        draw_label(draw, rect["x"]+5, rect["y"]+5,
                   f"Bedroom {i+1} ({bed['width']}x{bed['height']})")

        draw_door(draw, rect["x"]+bw, rect["y"]+bh//2, "right")
        draw_window(draw, rect["x"]+bw, rect["y"]+bh*0.25,
                    rect["x"]+bw, rect["y"]+bh*0.75)

        bedroom_positions.append({
            "index": i+1,
            **rect
        })

    # =========================
    # ATTACHED BATHROOMS (INSIDE BEDROOM)
    # =========================
    for bath in data["bathrooms"]["attached"]:
        bw, bh = bath["width"]*scale, bath["height"]*scale
        bed = next(b for b in bedroom_positions if b["index"] == bath["bedroom"])

        bx = bed["x"] + bed["w"] - bw - 8
        by = bed["y"] + 8

        if by + bh > bed["y"] + bed["h"]:
            by = bed["y"] + bed["h"] - bh - 8

        rect = clamp({"x": bx, "y": by, "w": bw, "h": bh}, margin, pw, ph)
        placed.append(rect)

        draw.rectangle([rect["x"], rect["y"], rect["x"]+bw, rect["y"]+bh],
                       outline="purple", width=3)
        draw_label(draw, rect["x"]+5, rect["y"]+5,
                   f"Bath (Attached) {bath['width']}x{bath['height']}")

        draw_door(draw, rect["x"], rect["y"]+bh//2, "left")
        draw_window(draw, rect["x"]+bw, rect["y"]+bh*0.25,
                    rect["x"]+bw, rect["y"]+bh*0.75)

    # =========================
    # COMMON BATHROOMS (CENTER)
    # =========================
    cx, cy = margin+pw*0.5, margin+ph*0.45

    for bath in data["bathrooms"]["common"]:
        bw, bh = bath["width"]*scale, bath["height"]*scale
        rect = auto_place({"x": cx, "y": cy, "w": bw, "h": bh}, placed,
                          margin+pw*0.7, margin+ph)
        rect = clamp(rect, margin, pw, ph)
        placed.append(rect)

        draw.rectangle([rect["x"], rect["y"], rect["x"]+bw, rect["y"]+bh],
                       outline="brown", width=3)
        draw_label(draw, rect["x"]+5, rect["y"]+5,
                   f"Bath (Common) {bath['width']}x{bath['height']}")

        draw_door(draw, rect["x"], rect["y"]+bh//2, "left")
        draw_window(draw, rect["x"]+bw, rect["y"]+bh*0.25,
                    rect["x"]+bw, rect["y"]+bh*0.75)

    # =========================
    # KITCHEN (EAST)
    # =========================
    if data["kitchen"]["size"]:
        kw, kh = data["kitchen"]["size"]
        kw, kh = kw*scale, kh*scale

        rect = auto_place({"x": margin+pw*0.65, "y": margin+80,
                           "w": kw, "h": kh}, placed,
                          margin+pw, margin+ph)
        rect = clamp(rect, margin, pw, ph)
        placed.append(rect)

        draw.rectangle([rect["x"], rect["y"], rect["x"]+kw, rect["y"]+kh],
                       outline="green", width=3)
        draw_label(draw, rect["x"]+5, rect["y"]+5,
                   f"Kitchen ({kw//scale}x{kh//scale})")

        draw_door(draw, rect["x"], rect["y"]+kh//2, "left")
        draw_window(draw, rect["x"]+kw, rect["y"]+kh*0.25,
                    rect["x"]+kw, rect["y"]+kh*0.75)

    # =========================
    # LIVING / DINING (SOUTH)
    # =========================
    lw, lh = data["living_dining"]["size"]
    lw, lh = lw*scale, lh*scale

    rect = auto_place({"x": margin+pw*0.35,
                       "y": margin+ph-lh-90,
                       "w": lw, "h": lh},
                      placed, margin+pw*0.8, margin+ph)
    rect = clamp(rect, margin, pw, ph)
    placed.append(rect)

    draw.rectangle([rect["x"], rect["y"], rect["x"]+lw, rect["y"]+lh],
                   outline="orange", width=3)
    draw_label(draw, rect["x"]+5, rect["y"]+5,
               f"Living/Dining ({lw//scale}x{lh//scale})")

    draw_door(draw, rect["x"]+lw//2, rect["y"]+lh, "down")
    draw_window(draw, rect["x"]+lw*0.25, rect["y"],
                rect["x"]+lw*0.75, rect["y"])

    living_rect = rect.copy()

    # =========================
    # BALCONY
    # =========================
    if "balcony" in data["extras"]:
        rect = clamp({
            "x": living_rect["x"],
            "y": living_rect["y"] + living_rect["h"] + 10,
            "w": 160,
            "h": 24
        }, margin, pw, ph)

        draw.rectangle([rect["x"], rect["y"],
                        rect["x"]+rect["w"], rect["y"]+rect["h"]],
                       outline="red", width=3)
        draw_label(draw, rect["x"]+10, rect["y"]+4, "Balcony")
        draw_window(draw, rect["x"]+10, rect["y"],
                    rect["x"]+rect["w"]-10, rect["y"])

    # =========================
    # NORTH ARROW
    # =========================
    nx, ny = margin+pw+40, margin+50
    draw.line([nx, ny, nx, ny-40], fill="black", width=3)
    draw.polygon([(nx-6, ny-40), (nx+6, ny-40), (nx, ny-52)], fill="black")
    draw.text((nx-8, ny-65), "N", fill="black")

    img.save(output_path)
