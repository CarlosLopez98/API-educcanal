from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Section, Course
from .article import *
from .quiz import *


put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="Name of the section is required", required=True)
put_args.add_argument("description", type=str, help="Description of the section is required", required=True)
put_args.add_argument("course_id", type=int, help="Course id of the section is required", required=True)

update_args = reqparse.RequestParser()
update_args.add_argument("name", type=str, help="Name of the section is required")
update_args.add_argument("description", type=str, help="Description of the section is required")
update_args.add_argument("course_id", type=int, help="Course id of the section is required")

class Articles(fields.Raw):
	def format(self, value):
		articles = []
		for val in value:
			article = ArticleResource.get(val.id)
			articles.append(article)
		return articles


class Quizzes(fields.Raw):
	def format(self, value):
		quizzes = []
		for val in value:
			quiz = QuizResource.get(val.id)
			quizzes.append(quiz)
		return quizzes


resource_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"description": fields.String,
	"course_id": fields.Integer,
	"articles": Articles,
	"quizzes": Quizzes
}


class SectionResource(Resource):
	@classmethod
	@marshal_with(resource_fields)
	def get(self, section_id):
		result = Section.get_by_id(section_id)

		if not result:
			abort(404, message="Could not find a section with that id")

		return result


class AllSectionResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Section.get_all()

		if not result:
			abort(404, message="Could not find any section")

		return result

	@marshal_with(resource_fields)
	def put(self):
		args = put_args.parse_args()

		course = Course.get_by_id(args['course_id'])

		if course is None:
			abort(409, message="Course id does not exists")

		section = Section(name=args['name'], description=args['description'],
							course_id=args['course_id'])

		Section.create_element(section)
		return section, 201