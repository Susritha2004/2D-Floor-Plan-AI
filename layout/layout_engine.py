def layout_rooms(data, scale=10, margin=60):
    plot_w, plot_h = data["plot_size"]
    pw, ph = plot_w*scale, plot_h*scale

    zones = {
        "bedroom": {
            "x": margin + 20,
            "y": margin + 40,
            "max_w": pw * 0.4
        },
        "bath": {
            "x": margin + pw * 0.45,
            "y": margin + 40,
            "max_w": pw * 0.2
        },
        "kitchen": {
            "x": margin + pw * 0.7,
            "y": margin + 40
        },
        "living": {
            "x": margin + pw * 0.35,
            "y": margin + ph * 0.6
        }
    }

    return zones
