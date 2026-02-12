def render_svg(layout, pw, ph, margin, door):
    canvas_w = pw + margin * 2
    canvas_h = ph + margin * 2

    svg = []
    svg.append(
        f'<svg width="{canvas_w}" height="{canvas_h}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )

    wall_thickness = 3
    door_size = 60  # width of door opening

    # =====================================================
    # OUTER WALL (with door gap)
    # =====================================================

    side, pos = door

    # Top wall
    if side == "top":
        svg.append(f'<line x1="{margin}" y1="{margin}" '
                   f'x2="{pos - door_size//2}" y2="{margin}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')
        svg.append(f'<line x1="{pos + door_size//2}" y1="{margin}" '
                   f'x2="{margin + pw}" y2="{margin}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')
    else:
        svg.append(f'<line x1="{margin}" y1="{margin}" '
                   f'x2="{margin + pw}" y2="{margin}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')

    # Bottom wall
    if side == "bottom":
        svg.append(f'<line x1="{margin}" y1="{margin + ph}" '
                   f'x2="{pos - door_size//2}" y2="{margin + ph}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')
        svg.append(f'<line x1="{pos + door_size//2}" y1="{margin + ph}" '
                   f'x2="{margin + pw}" y2="{margin + ph}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')
    else:
        svg.append(f'<line x1="{margin}" y1="{margin + ph}" '
                   f'x2="{margin + pw}" y2="{margin + ph}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')

    # Left wall
    if side == "left":
        svg.append(f'<line x1="{margin}" y1="{margin}" '
                   f'x2="{margin}" y2="{pos - door_size//2}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')
        svg.append(f'<line x1="{margin}" y1="{pos + door_size//2}" '
                   f'x2="{margin}" y2="{margin + ph}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')
    else:
        svg.append(f'<line x1="{margin}" y1="{margin}" '
                   f'x2="{margin}" y2="{margin + ph}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')

    # Right wall
    if side == "right":
        svg.append(f'<line x1="{margin + pw}" y1="{margin}" '
                   f'x2="{margin + pw}" y2="{pos - door_size//2}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')
        svg.append(f'<line x1="{margin + pw}" y1="{pos + door_size//2}" '
                   f'x2="{margin + pw}" y2="{margin + ph}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')
    else:
        svg.append(f'<line x1="{margin + pw}" y1="{margin}" '
                   f'x2="{margin + pw}" y2="{margin + ph}" '
                   f'stroke="black" stroke-width="{wall_thickness}"/>')

    # =====================================================
    # Draw Rooms
    # =====================================================

    for room in layout:

        # Room rectangle
        svg.append(
            f'<rect x="{room["x"]}" y="{room["y"]}" '
            f'width="{room["w"]}" height="{room["h"]}" '
            f'fill="{room.get("color", "#cccccc")}" '
            f'stroke="white" stroke-width="2"/>'
        )

        # Smart font size
        if room["w"] < 80 or room["h"] < 80:
            font_size = 11
        else:
            font_size = 14

        # Centered text
        text_x = room["x"] + room["w"] / 2
        text_y = room["y"] + room["h"] / 2

        svg.append(
            f'<text x="{text_x}" '
            f'y="{text_y}" '
            f'text-anchor="middle" '
            f'dominant-baseline="middle" '
            f'fill="white" '
            f'font-size="{font_size}" '
            f'pointer-events="none">'
            f'{room["name"]}</text>'
        )

    svg.append("</svg>")
    return "\n".join(svg)
