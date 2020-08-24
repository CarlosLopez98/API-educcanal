from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Quiz, Section


put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="Name of the quiz is required", required=True)
put_args.add_argument("section_id", type=int, help="Section id of the quiz is required", required=True)


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
	"section_id": fields.Integer,
	"questions": Questions
}


class QuizResource(Resource):
	@classmethod
	@marshal_with(resource_fields)
	def get(self, quiz_id):
		result = Quiz.get_by_id(quiz_id)

		if not result:
			abort(404, message="Could not find a quiz with that id")

		return result


class AllQuizResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Quiz.get_all()

		if not result:
			abort(404, message="Could not find any quiz")

		return result

	@marshal_with(resource_fields)
	def put(self):
		args = put_args.parse_args()
		
		section = Section.get_by_id(args['section_id'])

		if section is None:
			abort(409, message="Section id does not exists")

		quiz = Quiz(name=args['name'], section_id=args['section_id'])

		Quiz.create_element(quiz)
		return quiz, 201