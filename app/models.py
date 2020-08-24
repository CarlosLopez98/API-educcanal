from . import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime


# Modelos
class Subject(db.Model):
	__tablename__ = 'subjects'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.Text, nullable=True)
	courses = db.relationship('Course', lazy='dynamic')

	@classmethod
	def get_by_id(cls, id):
		return Subject.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Subject.query.all()


class Author(db.Model):
	__tablename__ = 'authors'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	surname = db.Column(db.String(50), nullable=False)
	mail = db.Column(db.String(100), nullable=False, unique=True)
	info = db.Column(db.Text, nullable=True)
	image = db.Column(db.String(150), nullable=True)
	courses = db.relationship('Course', lazy='dynamic')

	@classmethod
	def get_by_id(cls, id):
		return Author.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Author.query.all()


class Course(db.Model):
	__tablename__ = 'courses'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text, nullable=False)
	subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
	inscriptions = db.relationship('Inscription', lazy='dynamic')
	sections = db.relationship('Section', lazy='dynamic')

	@classmethod
	def create_element(cls, course):
		db.session.add(course)
		db.session.commit()

	@classmethod
	def get_by_id(cls, id):
		return Course.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Course.query.all()


class Section(db.Model):
	__tablename__ = 'sections'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.Text, nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
	articles = db.relationship('Article', lazy="dynamic")
	quizzes = db.relationship('Quiz', lazy='dynamic')

	@classmethod
	def create_element(cls, section):
		db.session.add(section)
		db.session.commit()

	@classmethod
	def get_by_id(cls, id):
		return Section.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Section.query.all()


class Article(db.Model):
	__tablename__ = 'articles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
	comments = db.relationship('Comment', lazy='dynamic')
	progress = db.relationship('Progress', lazy='dynamic')

	@classmethod
	def create_element(cls, section):
		db.session.add(section)
		db.session.commit()

	@classmethod
	def get_by_id(cls, id):
		return Article.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Article.query.all()


class Quiz(db.Model):
	__tablename__ = 'quizzes'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), unique=True)
	questions = db.relationship('Question', lazy='dynamic')

	@classmethod
	def create_element(cls, quiz):
		db.session.add(quiz)
		db.session.commit()

	@classmethod
	def get_by_id(cls, id):
		return Quiz.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Quiz.query.all()


class TypeQuestion(db.Model):
	__tablename__ = 'type_questions'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.Text, nullable=False)
	questions = db.relationship('Question', lazy='dynamic')

	@classmethod
	def get_by_id(cls, id):
		return TypeQuestion.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return TypeQuestion.query.all()


class Question(db.Model):
	__tablename__ = 'questions'

	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=False)
	quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
	type_quest_id = db.Column(db.Integer, db.ForeignKey('type_questions.id'))
	answers = db.relationship('Answer', lazy='dynamic')

	@classmethod
	def create_element(cls, question):
		db.session.add(question)
		db.session.commit()

	@classmethod
	def get_by_id(cls, id):
		return Question.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Question.query.all()


class Answer(db.Model):
	__tablename__ = 'answers'

	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=False)
	value = db.Column(db.Boolean, nullable=False)
	question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

	@classmethod
	def create_element(cls, answer):
		db.session.add(answer)
		db.session.commit()

	@classmethod
	def get_by_id(cls, id):
		return Answer.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Answer.query.all()


class Gender(db.Model):
	__tablename__ = 'genders'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(10), nullable=False)
	users = db.relationship('User', lazy='dynamic')

	@classmethod
	def get_by_id(cls, id):
		return Gender.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Gender.query.all()


class TypeUser(db.Model):
	__tablename__ = 'type_users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(15), nullable=False)
	users = db.relationship('User', lazy='dynamic')

	@classmethod
	def get_by_id(cls, id):
		return TypeUser.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return TypeUser.query.all()


class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	surname = db.Column(db.String(50), nullable=False)
	mail = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(94), nullable=False)
	image = db.Column(db.String(150), nullable=True)
	birthdate = db.Column(db.DateTime(), nullable=False)
	created_at = db.Column(db.DateTime(), default=datetime.today())
	updated_at = db.Column(db.DateTime(), nullable=True, default=datetime.today())
	gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
	type_user_id = db.Column(db.Integer, db.ForeignKey('type_users.id'))
	inscriptions = db.relationship('Inscription', lazy='dynamic')
	comments = db.relationship('Comment', lazy='dynamic')
	progress = db.relationship('Progress', lazy='dynamic')
	grades = db.relationship('Grade', lazy='dynamic')
	
	def verify_password(self, password):
		return check_password_hash(self.password, password)
	
	@property
	def un_password(self):
		pass

	@un_password.setter
	def un_password(self, value):
		self.password = generate_password_hash(value)

	@property
	def format_date(self):
		pass

	@format_date.setter
	def format_date(self, value):
		value = value.split('-')
		self.birthdate = datetime(int(value[0]), int(value[1]), int(value[2]))

	@classmethod
	def create_element(cls, user):
		db.session.add(user)
		db.session.commit()

	@classmethod
	def get_by_id(cls, id):
		return User.query.filter_by(id=id).first()

	@classmethod
	def get_by_mail(cls, mail):
		return User.query.filter_by(mail=mail).first()

	@classmethod
	def get_all(cls):
		return User.query.all()


class Comment(db.Model):
	__tablename__ = 'comments'

	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime(), default=datetime.today())
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
	comments = db.relationship('Comment', lazy='dynamic')

	@classmethod
	def get_by_id(cls, id):
		return Comment.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Comment.query.all()


class Progress(db.Model):
	__tablename__ = 'progress'

	id = db.Column(db.Integer, primary_key=True)
	complete = db.Column(db.Boolean, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

	@classmethod
	def get_by_id(cls, id):
		return Progress.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Progress.query.all()


class Inscription(db.Model):
	__tablename__ = 'inscriptions'

	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime(), default=datetime.today())
	last_enter = db.Column(db.DateTime(), default=datetime.today())
	progress = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
	reviews = db.relationship('Review', lazy='dynamic')

	@classmethod
	def get_by_id(cls, id):
		return Inscription.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Inscription.query.all()


class Review(db.Model):
	__tablename__ = 'reviews'

	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=True)
	calification = db.Column(db.Float, nullable=False)
	inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))

	@classmethod
	def get_by_id(cls, id):
		return Review.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Review.query.all()


class Grade(db.Model):
	__tablename__ = 'grades'

	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Float, nullable=False)
	usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))

	@classmethod
	def get_by_id(cls, id):
		return Grade.query.filter_by(id=id).first()

	@classmethod
	def get_all(cls):
		return Grade.query.all()