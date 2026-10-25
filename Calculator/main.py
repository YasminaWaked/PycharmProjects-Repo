from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "ABC987"
db = SQLAlchemy(app)


class History(db.Model):
    firstNum = db.Column(db.Integer, primary_key=True)
    secondNum = db.Column(db.Integer)
    op = db.Column(db.String(100))
    prevResult = db.Column(db.Integer())

    def __init__(self, firstNum, secondNum, op, prevResult):
        self.firstNum = firstNum
        self.secondNum = secondNum
        self.op = op
        self.prevResult = prevResult


@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    prevResult = result
    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
    return render_template("calculator.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
