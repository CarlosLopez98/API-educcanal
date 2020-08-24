from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Subject
from .course import *


class Courses(fields.Raw):
	def format(self, value):
		courses = []
		for val in value:
			course = CourseResource.get(val.id)
			courses.append(course)
		return courses

resource_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"description": fields.String,
	"courses": Courses
}


class SubjectResource(Resource):
	@marshal_with(resource_fields)
	def get(self, subject_id):
		result = Subject.get_by_id(subject_id)

		if not result:
			abort(404, message="Could not find a subject with that id")

		return result


class AllSubjectResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Subject.get_all()

		if not result:
			abort(404, message="Could not find any subject")

		return result