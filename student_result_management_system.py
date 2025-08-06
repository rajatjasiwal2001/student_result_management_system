from flask import Flask, render_template, redirect, request
import pymysql

app = Flask(__name__)

def connection():
    return pymysql.connect(
        host="localhost", user="root", password="", database="students"
    )

@app.route("/")
def home():
    return render_template("add_student.html")

@app.route("/add_student", methods=["POST"])
def add_student():
    conn = connection()
    id = request.form["id"]
    name = request.form["name"]
    subject = request.form["subject"]
    marks = request.form["marks"]
    with conn.cursor() as cur:
        sql = "INSERT INTO results(id, name, subject, marks) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (id, name, subject, marks))
        conn.commit()
    return redirect("/result_list")

@app.route("/result_list")
def result_list():
    conn = connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM results")
        data = cur.fetchall()
    return render_template("result_list.html", data=data)

@app.route("/delete/id=<int:id>")
def delete(id):
    conn = connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM results WHERE id=%s", (id,))
        conn.commit()
    return redirect("/result_list")

@app.route("/update_student/id=<int:id>")
def update_student(id):
    conn = connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM results WHERE id=%s", (id,))
        data = cur.fetchone()
    return render_template("update_student.html", data=data)

@app.route("/update_data", methods=["POST"])
def update_data():
    conn = connection()
    id = request.form["id"]
    name = request.form["name"]
    subject = request.form["subject"]
    marks = request.form["marks"]
    with conn.cursor() as cur:
        sql = "UPDATE results SET name=%s, subject=%s, marks=%s WHERE id=%s"
        cur.execute(sql, (name, subject, marks, id))
        conn.commit()
    return redirect("/result_list")

if __name__ == "__main__":
    app.run(debug=True)

