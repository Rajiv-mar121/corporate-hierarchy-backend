from flask import Flask
from flask_restful import Api
from models.employee import db
from web.employees import EmployeeItemResource, EmployeeListResource, EmployeeCSVResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///corporate_hierarchy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

api.add_resource(EmployeeListResource, '/employees')
api.add_resource(EmployeeItemResource, '/employee', '/employee/<int:id>')
api.add_resource(EmployeeCSVResource, '/employees/upload')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


# /mnt/c/Users/rajneesh.jha/coporate_hierarchy/instance/corporate_hierarchy.db