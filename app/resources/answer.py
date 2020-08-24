from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Answer, Question


put_args = reqparse.RequestParser()
put_args.add_argument("text", type=str, help="Text of the answer is required", required=True)
put_args.add_argument("value", type=bool, help="Value of the answer is required", required=True)
put_args.add_argument("question_id", type=int, help="Question of the answer is required", required=True)

resource_fields = {
    "id": fields.Integer,
    "text": fields.String,
    "value": fields.Boolean,
    "question_id": fields.Integer
}


class AnswerResource(Resource):
    @classmethod
    @marshal_with(resource_fields)
    def get(self, answer_id):
        result = Answer.get_by_id(answer_id)

        if not result:
            abort(404, message="Could not find a answer with that id")

        return result


class AllAnswerResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = Answer.get_all()

        if not result:
            abort(404, message="Could not find a answer with that id")

        return result

    @marshal_with(resource_fields)
    def put(self):
        args = put_args.parse_args()

        question = Question.get_by_id(args['question_id'])

        if question is None:
            abort(409, message="Question id does not exists")

        answer = Answer(text=args['text'], value=args['value'], 
                        question_id=args['question_id'])
        
        Answer.create_element(answer)
        return answer, 201