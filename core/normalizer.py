def normalize(data):
    # Ensure plot size exists
    if not data.get("plot_size"):
        data["plot_size"] = [40, 60]

    pw, ph = data["plot_size"]

    # Bedrooms
    bhk = data.get("bhk", 1)
    bedrooms = data.get("bedrooms", [])

    # Fill missing bedroom sizes
    for bed in bedrooms:
        if not bed.get("width"):
            bed["width"] = 10
        if not bed.get("height"):
            bed["height"] = 12

    # Add missing bedrooms if fewer than bhk
    while len(bedrooms) < bhk:
        bedrooms.append({
            "index": len(bedrooms) + 1,
            "width": 10,
            "height": 12
        })

    data["bedrooms"] = bedrooms

    # Kitchen defaults
    kitchen = data.get("kitchen", {})
    if not kitchen.get("width"):
        kitchen["width"] = 8
    if not kitchen.get("height"):
        kitchen["height"] = 10
    data["kitchen"] = kitchen

    # Living defaults
    living = data.get("living", {})
    if not living.get("width"):
        living["width"] = 12
    if not living.get("height"):
        living["height"] = 14
    data["living"] = living

    return data
