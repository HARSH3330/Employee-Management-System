from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Secret Key for Flask sessions and flash messages
app.config['SECRET_KEY'] = 'your_secret_key'
bcrypt = Bcrypt(app)

# Employee Class to store employee data in memory
class Employee:
    employee_list = []  # Store employee objects
    employee_ids = set()  # Store unique employee IDs

    def __init__(self, employee_id, name, department):
        if employee_id in Employee.employee_ids:
            raise ValueError("Employee ID must be unique.")
        self.employee_id = employee_id
        self.name = name
        self.department = department
        Employee.employee_ids.add(employee_id)
        Employee.employee_list.append(self)

    def display_employee(self):
        return f"Employee ID: {self.employee_id}, Name: {self.name}, Department: {self.department}"

    @staticmethod
    def display_all_employees():
        return Employee.employee_list

# Route to add employee through URL parameters
@app.route("/add_employee")
def add_employee():
    employee_id = request.args.get("employee_id")
    name = request.args.get("name")
    department = request.args.get("department")

    try:
        employee = Employee(employee_id, name, department)
        flash(f"Employee {employee.name} added successfully!", "success")
    except ValueError as e:
        flash(str(e), "danger")
    
    return redirect(url_for("home"))

# Route to display all employees
@app.route("/display_employees")
def display_employees():
    employees = Employee.display_all_employees()
    return render_template("display_employees.html", employees=employees)

# Home Route
@app.route("/home")
def home():
    return render_template("home.html")

# Index Page
@app.route("/")
def index():
    return render_template("index.html")

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return redirect(url_for("home"))
    return render_template("login.html")

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
