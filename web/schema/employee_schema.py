from marshmallow import Schema, fields, validate
from models.employee import Employee

class EmployeeSchema(Schema):
    id = fields.Integer(dump_only=True,)
    name = fields.String(required=True, validate=validate.Length(max=255))
    designation = fields.String(required=True)
    email = fields.String(required=True)
    department = fields.String(validate=validate.Length(max=255))
    team = fields.String(validate=validate.Length(max=255))
    manager_id = fields.Integer(allow_none=True)

    manager_name = fields.Method('get_manager_name', dump_only=True)

    def get_manager_name(self, obj):
        print(obj)
        if obj.manager:
            return obj.manager.name
        return None
