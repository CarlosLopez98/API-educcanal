from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Gender


resource_fields = {
	"id": fields.Integer,
	"name": fields.String
}

class GenderResource(Resource):
	@marshal_with(resource_fields)
	def get(self, gender_id):
		result = Gender.get_by_id(gender_id)

		if not result:
			abort(404, message="Could not find a gender with that id")

		return result


class AllGenderResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Gender.get_all()

		if not result:
			abort(404, message="Could not find any gender")

		return result