from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Author

resource_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"surname": fields.String,
	"mail": fields.String,
	"info": fields.String,
	"image": fields.String,
}


class AuthorResource(Resource):
	@marshal_with(resource_fields)
	def get(self, author_id):
		result = Author.get_by_id(author_id)

		if not result:
			abort(404, message="Could not find an author with that id")

		return result


class AllAuthorResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Author.get_all()

		if not result:
			abort(404, message="Could not find any author")

		return result