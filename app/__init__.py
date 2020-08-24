from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
db = SQLAlchemy()
api = Api(app)
cors = CORS(app)

from .models import *
from .views import *
from .resources import *


# Recursos
api.add_resource(AllAuthorResource, '/authors')
api.add_resource(AuthorResource, '/authors/<int:author_id>')

api.add_resource(AllSubjectResource, '/subjects')
api.add_resource(SubjectResource, '/subjects/<int:subject_id>')

api.add_resource(AllCourseResource, '/courses')
api.add_resource(CourseResource, '/courses/<int:course_id>')

api.add_resource(AllSectionResource, '/sections')
api.add_resource(SectionResource, '/sections/<int:section_id>')

api.add_resource(AllArticleResource, '/articles')
api.add_resource(ArticleResource, '/articles/<int:article_id>')

api.add_resource(AllQuizResource, '/quizzes')
api.add_resource(QuizResource, '/quizzes/<int:quiz_id>')

api.add_resource(AllTypeQuestionResource, '/questions/type')
api.add_resource(TypeQuestionResource, '/questions/type/<int:type_question_id>')

api.add_resource(AllQuestionResource, '/questions')
api.add_resource(QuestionResource, '/questions/<int:question_id>')

api.add_resource(AllAnswerResource, '/answers')
api.add_resource(AnswerResource, '/answers/<int:answer_id>')

api.add_resource(AllGenderResource, '/genders')
api.add_resource(GenderResource, '/genders/<int:gender_id>')

api.add_resource(AllTypeUserResource, '/users/types')
api.add_resource(TypeUserResource, '/users/types/<int:type_user_id>')

api.add_resource(AllUserResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(VerifyUserResource, '/users/auth')


def create_app(config):
	app.config.from_object(config)

	app.app_context().push()

	with app.app_context():
		db.init_app(app)
		db.create_all()

	return app