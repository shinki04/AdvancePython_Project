from flask import Flask, render_template, request, redirect, session, flash
from flask_bootstrap import Bootstrap
from model import Database  
import os

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "AFCAHNF&A*@435"  # For session management

# Configure database connection

db = Database("quanlysinhvien", "postgres", "123456", "localhost", "5432", "sinhvien")
db.connect_db()

# Routes
@app.route("/")
def index():
    if "username" in session:
        return redirect("/students")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # if db.validate_user(username, password):
        #     session["username"] = username
        #     return redirect("/students")
        # else:
        #     flash("Invalid username or password", "danger")
        if username == "postgres" and password =="123456":
            session["username"] = username
            return redirect("/students")
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

@app.route("/students", methods=["GET", "POST"])
def students():
    if "username" not in session:
        return redirect("/login")
    if request.method == "POST":
        mssv = request.form.get("mssv")
        ho = request.form.get("ho")
        ten = request.form.get("ten")
        image = request.files["image"]
        image_path = os.path.join("uploads", image.filename)
        image.save(image_path)
        if db.insert_data(mssv, ho, ten, image_path):
            flash("Student added successfully", "success")
        else:
            flash("Error adding student", "danger")
    students = db.load_data()
    return render_template("students.html", students=students)

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if "username" not in session:
        return redirect("/login")
    if request.method == "POST":
        mssv = request.form.get("mssv")
        ho = request.form.get("ho")
        ten = request.form.get("ten")
        image = request.files["image"]
        image_path = os.path.join("uploads", image.filename)
        image.save(image_path)
        if db.insert_data(mssv, ho, ten, image_path):
            flash("Student added successfully", "success")
        else:
            flash("Error adding student", "danger")
        return redirect("/students")
    return render_template("add_student.html")

@app.route("/edit_student/<string:mssv>", methods=["GET", "POST"])
def edit_student(mssv):
    if "username" not in session:
        return redirect("/login")
    if request.method == "POST":
        ho = request.form.get("ho")
        ten = request.form.get("ten")
        image = request.files.get("image")
        image_path = None
        if image:
            image_path = os.path.join("uploads", image.filename)
            image.save(image_path)
        if db.update_data(mssv, ho, ten, image_path):
            flash("Student updated successfully", "success")
        else:
            flash("Error updating student", "danger")
        return redirect("/students")
    student = db.get_student_by_mssv(mssv)  # Retrieve student details
    return render_template("edit_student.html", student=student)

@app.route("/delete_student/<string:mssv>")
def delete_student(mssv):
    if "username" not in session:
        return redirect("/login")
    if db.delete_data(mssv):
        flash("Student deleted successfully", "success")
    else:
        flash("Error deleting student", "danger")
    return redirect("/students")

if __name__ == "__main__":
    if not os.path.exists("/uploads"):
        os.mkdir("/uploads")
    app.run(debug=True,port=5050)
