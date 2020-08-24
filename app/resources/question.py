from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Question, Quiz, TypeQuestion
from .answer import AnswerResource


put_args = reqparse.RequestParser()
put_args.add_argument("text", type=str, help="Text of the question is required", required=True)
put_args.add_argument("quiz_id", type=int, help="Quiz id of the question is required", required=True)
put_args.add_argument("type_question_id", type=int, help="Question type id of the question is required", required=True)


class Answers(fields.Raw):
	def format(self, value):
		answers = []
		for val in value:
			answer = AnswerResource.get(val.id)
			answers.append(answer)
		return answers

resource_fields = {
	"id": fields.Integer,
	"text": fields.String,
	"quiz_id": fields.Integer,
	"type_quest_id": fields.Integer,
	"answers": Answers
}


class QuestionResource(Resource):
	@classmethod
	@marshal_with(resource_fields)
	def get(self, question_id):
		result = Question.get_by_id(question_id)

		if not result:
			abort(404, message="Could not find a question with that id")

		return result


class AllQuestionResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Question.get_all()

		if not result:
			abort(404, message="Could not find any questions")

		return result

	@marshal_with(resource_fields)
	def put(self):
		args = put_args.parse_args()

		quiz = Quiz.get_by_id(args['quiz_id'])
		type_question = TypeQuestion.get_by_id(args['type_question_id'])

		if quiz is None:
			abort(409, message="Quiz id does not exists")

		if type_question is None:
			abort(409, message="Question type does not exists")

		question = Question(text=args['text'], quiz_id=args['quiz_id'], 
							type_quest_id=args['type_question_id'])

		Question.create_element(question)
		return question, 201
