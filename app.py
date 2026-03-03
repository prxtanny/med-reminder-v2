from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# ⚠️ ห้ามใส่ debug=True บน production
# ⚠️ ห้ามกำหนด port เอง
