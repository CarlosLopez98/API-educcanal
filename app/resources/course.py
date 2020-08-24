from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Course, Subject, Author
from .section import *


put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="Name of the course is required", required=True)
put_args.add_argument("description", type=str, help="Description of the course is required", required=True)
put_args.add_argument("subject_id", type=int, help="Subject id of the course is required", required=True)
put_args.add_argument("author_id", type=int, help="Author id of the course is required", required=True)

class Sections(fields.Raw):
	def format(self, value):
		sections = []
		for val in value:
			section = SectionResource.get(val.id)
			sections.append(section)
		return sections


resource_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"description": fields.String,
	"subject_id": fields.Integer,
	"author_id": fields.Integer,
	"sections": Sections
}


class CourseResource(Resource):
	@classmethod
	@marshal_with(resource_fields)
	def get(self, course_id):
		result = Course.get_by_id(course_id)

		if not result:
			abort(404, message="Could not find a course with that id")

		return result


class AllCourseResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Course.get_all()

		if not result:
			abort(404, message="Could not find any course")

		return result

	@marshal_with(resource_fields)
	def put(self):
		args = put_args.parse_args()

		subject = Subject.get_by_id(args['subject_id'])
		author = Author.get_by_id(args['author_id'])

		if subject is None:
			abort(409, message="Subject id does not exist")

		if author is None:
			abort(409, message="Author id does not exist")		

		course = Course(name=args['name'], description=args['description'],
						subject_id=args['subject_id'], author_id=args['author_id'])

		Course.create_element(course)
		return course, 201