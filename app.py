from flask import Flask, render_template
from database import fetch_statistics

app = Flask(__name__)

@app.route("/")
def index():
    stats = fetch_statistics()
    return render_template("index.html", stats=stats)

if __name__ == "__main__":
    app.run(debug=True)