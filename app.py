# app.py
from flask import Flask, render_template, request
from chatbot import frage_verarbeiten, sql_ausführen

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    antwort = None
    sql_query = ""
    if request.method == "POST":
        frage = request.form["frage"]
        db_typ = request.form["db_typ"]
        sql_query = frage_verarbeiten(frage, db_typ)
        antwort = sql_ausführen(sql_query, db_typ)
    return render_template("index.html", antwort=antwort, sql_query=sql_query)



if __name__ == "__main__":
    app.run(debug=True)
