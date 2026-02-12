def generate_layout(data, scale=10, margin=60):
    plot_w, plot_h = data["plot_size"]
    facing = data.get("facing", "north")

    pw, ph = plot_w * scale, plot_h * scale
    layout = []

    half_w = pw // 2
    half_h = ph // 2

    # Quadrants
    TOP_LEFT = {"x": margin, "y": margin, "w": half_w, "h": half_h}
    TOP_RIGHT = {"x": margin + half_w, "y": margin, "w": half_w, "h": half_h}
    BOTTOM_LEFT = {"x": margin, "y": margin + half_h, "w": half_w, "h": half_h}
    BOTTOM_RIGHT = {"x": margin + half_w, "y": margin + half_h, "w": half_w, "h": half_h}

    # =================================================
    # Living → TOP RIGHT
    # =================================================
    living = TOP_RIGHT

    layout.append({
        "name": "Living / Hall",
        "color": "#a67c00",
        **living
    })

    # Door centered on living wall
    if facing == "north":
        door = ("top", living["x"] + living["w"] // 2)
    elif facing == "south":
        door = ("bottom", living["x"] + living["w"] // 2)
    elif facing == "east":
        door = ("right", living["y"] + living["h"] // 2)
    else:
        door = ("left", living["y"] + living["h"] // 2)

    # =================================================
    # Kitchen → BOTTOM RIGHT
    # =================================================
    layout.append({
        "name": "Kitchen",
        "color": "#1e5631",
        **BOTTOM_RIGHT
    })

    # =================================================
    # Bedrooms → LEFT SIDE
    # =================================================
    bedrooms = data.get("bedrooms", [])
    total = len(bedrooms)
    common_strip_width = 80

    # Master Bedroom
    if total >= 1:
        layout.append({
            "name": "Master Bedroom",
            "color": "#2f3640",
            **BOTTOM_LEFT
        })

    # 2BHK Case
    if total == 2:
        layout.append({
            "name": "Bedroom 2",
            "x": TOP_LEFT["x"],
            "y": TOP_LEFT["y"],
            "w": TOP_LEFT["w"] - common_strip_width,
            "h": TOP_LEFT["h"],
            "color": "#3a3f44"
        })

    # More than 2 Bedrooms
    elif total > 2:
        remaining = total - 1
        stack_h = TOP_LEFT["h"] // remaining

        for i in range(remaining):
            layout.append({
                "name": f"Bedroom {i+2}",
                "x": TOP_LEFT["x"],
                "y": TOP_LEFT["y"] + i * stack_h,
                "w": TOP_LEFT["w"] - common_strip_width,
                "h": stack_h,
                "color": "#3a3f44"
            })

    # =================================================
    # Common Bathrooms
    # =================================================
    common = data.get("bathrooms", {}).get("common", [])
    count_common = len(common)

    if count_common > 0:
        each_h = TOP_LEFT["h"] // count_common

        for i in range(count_common):
            layout.append({
                "name": "Bathroom",
                "x": TOP_LEFT["x"] + TOP_LEFT["w"] - common_strip_width,
                "y": TOP_LEFT["y"] + i * each_h,
                "w": common_strip_width,
                "h": each_h,
                "color": "#555555"
            })

    # =================================================
    # Attached Bathrooms
    # =================================================
    attached = data.get("bathrooms", {}).get("attached", [])

    for bath in attached:
        bed_index = bath.get("bedroom", 1)

        if bed_index == 1:
            zone = BOTTOM_LEFT
        elif total == 2:
            zone = {
                "x": TOP_LEFT["x"],
                "y": TOP_LEFT["y"],
                "w": TOP_LEFT["w"] - common_strip_width,
                "h": TOP_LEFT["h"]
            }
        else:
            remaining = total - 1
            stack_h = TOP_LEFT["h"] // remaining
            i = bed_index - 2

            if i < 0 or i >= remaining:
                continue

            zone = {
                "x": TOP_LEFT["x"],
                "y": TOP_LEFT["y"] + i * stack_h,
                "w": TOP_LEFT["w"] - common_strip_width,
                "h": stack_h
            }

        bath_size = min(zone["w"], zone["h"]) // 3
        padding = 8

        layout.append({
            "name": "Bathroom",
            "x": zone["x"] + zone["w"] - bath_size - padding,
            "y": zone["y"] + padding,
            "w": bath_size,
            "h": bath_size,
            "color": "#777777"
        })

    # =================================================
    # Extras (Balcony / Storage / Stairs)
    # =================================================
    extras = data.get("extras", [])

    # Balcony → Outside Living
    for item in extras:
        if "balcony" in item.lower():
            layout.append({
                "name": "Balcony",
                "x": living["x"] + living["w"] // 2 - 50,
                "y": living["y"] - 30,
                "w": 100,
                "h": 25,
                "color": "#aa0000"
            })

    # Storage → Inside Kitchen
    for item in extras:
        if "storage" in item.lower():
            layout.append({
                "name": "Storage",
                "x": BOTTOM_RIGHT["x"] + 15,
                "y": BOTTOM_RIGHT["y"] + 15,
                "w": 70,
                "h": 70,
                "color": "#444444"
            })

    # Stairs → Outside Right of House
    for item in extras:
        if "stairs" in item.lower():
            layout.append({
                "name": "Stairs",
                "x": margin + pw + 20,
                "y": margin + ph // 2 - 50,
                "w": 80,
                "h": 100,
                "color": "#555555"
            })

    return layout, pw, ph, margin, door
