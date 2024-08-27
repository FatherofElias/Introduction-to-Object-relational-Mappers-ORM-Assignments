
# Task 1 --- Initialize and Setup Flask app in venv.


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Elias928@localhost/fitness_db'
db = SQLAlchemy(app)

class Member(db.Model):
    __tablename__ = 'Members'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class WorkoutSession(db.Model):
    __tablename__ = 'WorkoutSessions'
    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id'), nullable=False)
    session_date = db.Column(db.String(50), nullable=False)
    session_time = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(100), nullable=False)

    member = db.relationship('Member', backref=db.backref('workout_sessions', lazy=True))

# Task 2 --- Implement CRUD Operations For Members

# Route to add a new member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], age=data['age'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "Member added successfully!"}), 201

# Route to retrieve a member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get_or_404(id)
    return jsonify({"id": member.id, "name": member.name, "age": member.age}), 200

# Route to update a member by ID
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    member = Member.query.get_or_404(id)
    member.name = data['name']
    member.age = data['age']
    db.session.commit()
    return jsonify({"message": "Member updated successfully!"}), 200

# Route to delete a member by ID
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted successfully!"}), 200


# Task 3 ----

# Route to add a new workout session
@app.route('/workouts', methods=['POST'])
def add_workout_session():
    data = request.get_json()
    new_session = WorkoutSession(
        member_id=data['member_id'],
        session_date=data['session_date'],
        session_time=data['session_time'],
        activity=data['activity']
    )
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"message": "Workout session added successfully!"}), 201

# Route to update a workout session by ID
@app.route('/workouts/<int:session_id>', methods=['PUT'])
def update_workout_session(session_id):
    data = request.get_json()
    session = WorkoutSession.query.get_or_404(session_id)
    session.member_id = data['member_id']
    session.session_date = data['session_date']
    session.session_time = data['session_time']
    session.activity = data['activity']
    db.session.commit()
    return jsonify({"message": "Workout session updated successfully!"}), 200

# Route to view all workout sessions
@app.route('/workouts', methods=['GET'])
def get_all_workout_sessions():
    sessions = WorkoutSession.query.all()
    result = [{
        "session_id": session.session_id,
        "member_id": session.member_id,
        "session_date": session.session_date,
        "session_time": session.session_time,
        "activity": session.activity
    } for session in sessions]
    return jsonify(result), 200

# Route to retrieve all workout sessions for a specific member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_workout_sessions_for_member(member_id):
    sessions = WorkoutSession.query.filter_by(member_id=member_id).all()
    result = [{
        "session_id": session.session_id,
        "member_id": session.member_id,
        "session_date": session.session_date,
        "session_time": session.session_time,
        "activity": session.activity
    } for session in sessions]
    return jsonify(result), 200


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)