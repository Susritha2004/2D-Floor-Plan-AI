from flask import Flask, render_template, request, jsonify
from layout.parser import parse_chatbot_data
from render.draw_floorplan import draw_floorplan

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    raw_data = request.json
    structured_data = parse_chatbot_data(raw_data)

    draw_floorplan(structured_data)

    return jsonify({
        "status": "success",
        "image_url": "/static/floorplan.png",
        "structured_data": structured_data
    })

if __name__ == "__main__":
    app.run(debug=True)
