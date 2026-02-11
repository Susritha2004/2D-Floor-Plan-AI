import re

def extract_dimensions(text):
    nums = re.findall(r"\d+", text)
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    return None, None


def parse_chatbot_data(data):
    parsed = {}

    # 1️⃣ BHK
    bhk_match = re.search(r"\d+", data.get("step_1", ""))
    parsed["bhk"] = int(bhk_match.group()) if bhk_match else 1

    # 2️⃣ Plot size
    pw, ph = extract_dimensions(data.get("step_2", ""))
    if not pw or not ph:
        raise ValueError("Invalid plot size")
    parsed["plot_size"] = [pw, ph]

    # 3️⃣ Shape
    parsed["shape"] = data.get("step_3", "").lower()

    # 4️⃣ Bedrooms (STANDARDIZED)
    bedrooms = []
    bed_text = data.get("step_4", "")

    for i, part in enumerate(bed_text.split(",")):
        w, h = extract_dimensions(part)
        if w and h:
            bedrooms.append({
                "index": i + 1,
                "width": w,
                "height": h
            })

    parsed["bedrooms"] = bedrooms

    # 5️⃣ Attached bathrooms
    attached = []
    attached_text = data.get("step_5", "").lower()

    # Example: bedroom 1 5x8
    matches = re.findall(r"bedroom\s*(\d+)\s*(\d+)\s*x\s*(\d+)", attached_text)
    for m in matches:
        attached.append({
            "bedroom": int(m[0]),
            "width": int(m[1]),
            "height": int(m[2])
        })

    # 6️⃣ Common bathrooms
    common = []
    common_text = data.get("step_6", "").lower()

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

    # 7️⃣ Kitchen
    kitchen_text = data.get("step_7", "").lower()
    kw, kh = extract_dimensions(kitchen_text)
    parsed["kitchen"] = {
        "type": "open" if "open" in kitchen_text else "closed",
        "size": [kw, kh] if kw and kh else None
    }

    # 8️⃣ Living / Dining
    living_text = data.get("step_8", "").lower()
    lw, lh = extract_dimensions(living_text)
    parsed["living_dining"] = {
        "type": "combined" if "combined" in living_text else "separate",
        "size": [lw, lh] if lw and lh else None
    }

    # 9️⃣ Extras
    extras_text = data.get("step_9", "")
    parsed["extras"] = [x.strip().lower() for x in extras_text.split(",") if x.strip()]

    return parsed
