import re


def extract_dimensions(text):
    nums = re.findall(r"\d+", text or "")
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    return None, None


def parse_chatbot_steps(data):
    if not data:
        return {}

    parsed = {}

    # 1️⃣ BHK
    bhk_match = re.search(r"\d+", data.get("step_1", "") or "")
    parsed["bhk"] = int(bhk_match.group()) if bhk_match else 1

    # 2️⃣ Plot Size
    pw, ph = extract_dimensions(data.get("step_2", ""))
    parsed["plot_size"] = [pw, ph] if pw and ph else [40, 60]

    # 3️⃣ Facing
    facing = (data.get("step_3", "north") or "").lower()
    if facing not in ["north", "south", "east", "west"]:
        facing = "north"
    parsed["facing"] = facing

    # 4️⃣ Shape
    parsed["shape"] = (data.get("step_4", "rectangle") or "").lower()

    # 5️⃣ Bedrooms
    bedrooms = []
    bed_text = data.get("step_5", "") or ""

    for i, part in enumerate(bed_text.split(",")):
        w, h = extract_dimensions(part)
        bedrooms.append({
            "index": i + 1,
            "width": w,
            "height": h
        })

    parsed["bedrooms"] = bedrooms

    # 6️⃣ Attached Bathrooms
    attached = []
    attached_text = (data.get("step_6", "") or "").lower()

    matches = re.findall(
        r"bedroom\s*(\d+)[^\d]*(\d+)\s*x\s*(\d+)",
        attached_text
    )

    for m in matches:
        attached.append({
            "bedroom": int(m[0]),
            "width": int(m[1]),
            "height": int(m[2])
        })

    # 7️⃣ Common Bathrooms
    common = []
    common_text = (data.get("step_7", "") or "").lower()

    matches = re.findall(r"(\d+)\s*x\s*(\d+)", common_text)
    for m in matches:
        common.append({
            "width": int(m[0]),
            "height": int(m[1])
        })

    parsed["bathrooms"] = {
        "attached": attached,
        "common": common
    }

    # 8️⃣ Kitchen
    kitchen_text = (data.get("step_8", "") or "").lower()
    kw, kh = extract_dimensions(kitchen_text)

    parsed["kitchen"] = {
        "width": kw,
        "height": kh
    }

    # 9️⃣ Living
    living_text = (data.get("step_9", "") or "").lower()
    lw, lh = extract_dimensions(living_text)

    parsed["living"] = {
        "width": lw,
        "height": lh
    }

    # 🔟 Extras
    extras_text = data.get("step_10", "") or ""
    parsed["extras"] = [
        x.strip().lower()
        for x in extras_text.split(",")
        if x.strip()
    ]

    return parsed
