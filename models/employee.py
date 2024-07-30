from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    designation = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    team = db.Column(db.String(255), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    

    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email':self.email,
            'designation': self.designation,
            'department': self.department,
            'manager_id': self.manager.name if self.manager else None,
            'team': self.team
        }
