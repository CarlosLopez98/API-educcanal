from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import TypeQuestion
from .question import QuestionResource


put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="Name of the question type is required", required=True)
put_args.add_argument("description", type=str, help="Description of the question type is required", required=True)


class Questions(fields.Raw):
	def format(self, value):
		questions = []
		for val in value:
			question = QuestionResource.get(val.id)
			questions.append(question)
		return questions

resource_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"description": fields.String,
	"questions": Questions
}


class TypeQuestionResource(Resource):
	@classmethod
	@marshal_with(resource_fields)
	def get(self, type_question_id):
		result = TypeQuestion.get_by_id(type_question_id)

		if not result:
			abort(404, message="Could not find a question type with that id")

		return result


class AllTypeQuestionResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = TypeQuestion.get_all()

		if not result:
			abort(404, message="Could not find any question type")

		return result