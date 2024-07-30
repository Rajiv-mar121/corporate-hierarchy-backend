
import pandas as pd

from flask import request
from flask_restful import Resource

from models.employee import db, Employee
from web.schema.employee_schema import EmployeeSchema

employee_schema = EmployeeSchema()

class EmployeeListResource(Resource):
    def get(self):
        employees = Employee.query.all()
        return EmployeeSchema(many=True).dump(employees)

    def post(self):
        data = request.get_json()
        errors = employee_schema.validate(data)
        if errors:
            return {"Error":errors}

        new_employee = Employee(
            name=data['name'],
            designation=data['designation'],
            email=data['email'],
            department=data.get('department'),
            manager_id=data.get('manager_id'),
            team=data.get('team')
        )
        db.session.add(new_employee)
        db.session.commit()
        return {'message': 'Employee Added'}


class EmployeeItemResource(Resource):
    def get(self, id):
        employee = Employee.query.get(id)
        if not employee:
            return {'message': 'Employee Not Found!'}
        return employee_schema.dump(employee)

    def put(self, id):
        data = request.get_json()
        employee = Employee.query.get(id)
        errors = employee_schema.validate(data)
        if errors:
            return {"Errors":errors}

        if not employee:
            return {'message': 'Employee not found!'}

        employee.name = data['name']
        employee.designation = data['designation']
        employee.department = data.get('department')
        employee.manager_id = data.get('manager_id')
        employee.email=data.get('email'),
        employee.reporting_manager_id = data.get('reporting_manager_id')
        employee.team = data.get('team')
        db.session.commit()
        return {'message': 'Employee Updated!'}

    def delete(self, id):
        employee = Employee.query.get(id)
        if not employee:
            return {'message': 'Employee not found!'}

        db.session.delete(employee)
        db.session.commit()
        return {'message': 'Employee Deleted!'}


class EmployeeCSVResource(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}

        if file and file.filename.endswith('.csv'):
            try:
                data = pd.read_csv(file)
                required_columns = {'name', 'designation', 'department', 'manager_id', 'reporting_manager_id', 'team'}
                if not required_columns.issubset(data.columns):
                    return {'message': f'Missing required columns: {required_columns - set(data.columns)}'}

                errors = []
                new_employees = []
                for index, row in data.iterrows():
                    try:
                        employee_data = employee_schema.load(row.to_dict())
                        new_employee = Employee(**employee_data)
                        new_employees.append(new_employee)
                    except Exception as e:
                        errors.append(f'Row {index + 1}: {str(e)}')

                if errors:
                    return {'message': 'Validation errors', 'errors': errors}, 400

                db.session.bulk_save_objects(new_employees)
                db.session.commit()
                return {'message': 'Employees Added'}

            except Exception as e:
                return {'message': str(e)}

        return {'message': 'Invalid file format. Please upload a correct CSV file.'}
