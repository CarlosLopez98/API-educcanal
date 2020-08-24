from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import TypeUser


resource_fields = {
	"id": fields.Integer,
	"name": fields.String
}

class TypeUserResource(Resource):
	@marshal_with(resource_fields)
	def get(self, type_user_id):
		result = TypeUser.get_by_id(type_user_id)

		if not result:
			abort(404, message="Could not find a user type with that id")

		return result


class AllTypeUserResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = TypeUser.get_all()

		if not result:
			abort(404, message="Could not find any user type")

		return result