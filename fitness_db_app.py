from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Task 1 --- Initialize and Setup Flask app in venv.


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Elias928@localhost/fitness_db'
db = SQLAlchemy(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class WorkoutSession(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    session_date = db.Column(db.String(50), nullable=False)
    session_time = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(100), nullable=False)

    member = db.relationship('Member', backref=db.backref('workout_sessions', lazy=True))




with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
 app.run(debug=True)