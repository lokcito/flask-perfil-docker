import os
from flask import Flask, render_template

app = Flask(__name__)

DEBUG = os.environ.get("DEBUG", "TRUE") == "TRUE"

@app.route("/")
def home():
    return render_template('index.html', title='Equisd')

if __name__ == "__main__":
    print(f"running debug as {DEBUG}")
    app.run(debug=DEBUG)
