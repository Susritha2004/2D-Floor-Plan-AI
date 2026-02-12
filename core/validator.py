def validate(data):
    plot = data.get("plot_size")
    bedrooms = data.get("bedrooms", [])

    if not plot or len(plot) != 2:
        raise ValueError("Invalid plot size")

    pw, ph = plot

    if not isinstance(pw, int) or not isinstance(ph, int):
        raise ValueError("Plot dimensions must be integers")

    if pw <= 0 or ph <= 0:
        raise ValueError("Invalid plot size")

    if len(bedrooms) == 0:
        raise ValueError("At least one bedroom required")

    plot_area = pw * ph

    bed_area = 0
    for b in bedrooms:
        w = b.get("width")
        h = b.get("height")

        if w and h:
            bed_area += w * h

    if bed_area > plot_area:
        raise ValueError("Bedrooms exceed plot area")

    return True
