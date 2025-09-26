from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
