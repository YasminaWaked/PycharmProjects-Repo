from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)


@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
def add_students():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        student = Student(name=name, age=age)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_students(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', student=student)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
