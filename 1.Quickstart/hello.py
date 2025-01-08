from markupsafe import escape
from flask import Flask

app = Flask(__name__)

@app.route("/")  # This handles the root URL
def index():
    return "Hello, World!"

@app.route("/<name>")  # This handles URLs with a name
def hello(name):
    return f"Hello, {escape(name)}!"

if __name__ == "__main__":
    app.run(debug=True)
