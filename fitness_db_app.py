from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Task 1 --- Initialize and Setup Flask app in venv.


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Elias928@localhost/fitness_db'
db = SQLAlchemy(app)


class Member(db.Model):
    __tablename__ = 'Members'  # Explicitly specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class WorkoutSession(db.Model):
    __tablename__ = 'WorkoutSessions'  # Explicitly specify the table name
    session_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id'), nullable=False)
    session_date = db.Column(db.String(50), nullable=False)
    session_time = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(100), nullable=False)

    member = db.relationship('Member', backref=db.backref('workout_sessions', lazy=True))


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

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
 app.run(debug=True)