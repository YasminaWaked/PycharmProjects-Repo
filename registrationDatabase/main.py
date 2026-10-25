from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "ABC987"
db = SQLAlchemy(app)


# Create a table
class students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    dob = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    school = db.Column(db.String(100))
    bio = db.Column(db.String(150))
    interest = db.Column(db.String(50))
    week = db.Column(db.String(10))

    def __init__(self, name, age, dob, gender, school, bio, interest, week):
        self.name = name
        self.age = age
        self.dob = dob
        self.gender = gender
        self.school = school
        self.bio = bio
        self.interest = interest
        self.week = week


@app.route('/', methods=['GET', 'POST'])
def add_students():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        dob = request.form['dob']
        gender = request.form['gender']
        school = request.form['school']
        bio = request.form['bio']
        interest = request.form['interest']
        week = request.form['week']
        student = students(name, age, dob, gender, school, bio, interest, week)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('show_details'))
    return render_template('add_students.html')


@app.route('/show_details')
def show_details():
    Students = students.query.all()
    return render_template('show_details.html', students=Students)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port='8081')
