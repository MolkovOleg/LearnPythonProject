from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def first_page():
    fake_data = {"kek": "lol"}
    return render_template("kek.html", fake_data=fake_data)

if __name__ == "__main__":
    app.run(debug=True)