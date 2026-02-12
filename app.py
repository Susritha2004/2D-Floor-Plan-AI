from flask import Flask, render_template, request, Response, jsonify
import os

from chatbot.step_parser import parse_chatbot_steps
from core.normalizer import normalize
from core.validator import validate
from layout.layout_engine import generate_layout
from render.svg_renderer import render_svg

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        raw_data = request.get_json(silent=True)

        if not raw_data:
            return jsonify({"status": "error", "message": "Invalid input"}), 400

        structured_data = parse_chatbot_steps(raw_data)
        structured_data = normalize(structured_data)
        validate(structured_data)

        layout, pw, ph, margin, door = generate_layout(structured_data)
        svg = render_svg(layout, pw, ph, margin, door)

        # ✅ Ensure static folder exists
        os.makedirs("static", exist_ok=True)

        # ✅ Save SVG to static folder
        file_path = os.path.join("static", "floorplan.svg")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(svg)

        return Response(svg, mimetype="image/svg+xml")

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
