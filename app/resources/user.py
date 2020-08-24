from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import User, Gender, TypeUser
from datetime import datetime


put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="Name of the user is required", required=True)
put_args.add_argument("surname", type=str, help="Surname of the user are required", required=True)
put_args.add_argument("mail", type=str, help="Mail of the user is required", required=True)
put_args.add_argument("password", type=str, help="Password of user is required", required=True)
put_args.add_argument("image", type=str)
put_args.add_argument("birthdate", type=str, help="Birthdate of the user is required", required=True)
put_args.add_argument("gender_id", type=int, help="Gender id from user is required", required=True)
put_args.add_argument("type_user_id", type=int, help="Type of user is required", required=True)

update_args = reqparse.RequestParser()
update_args.add_argument("name", type=str, help="Name of the user is required")
update_args.add_argument("surname", type=str, help="Surname of the user are required")
update_args.add_argument("mail", type=str, help="Mail of the user is required")
update_args.add_argument("password", type=str, help="Password of user is required")
update_args.add_argument("image", type=str)
update_args.add_argument("birthdate", type=str, help="Birthdate of the user is required")
update_args.add_argument("gender_id", type=int, help="Gender id from user is required")
update_args.add_argument("type_user_id", type=int, help="Type of user is required")

verify_args = reqparse.RequestParser()
verify_args.add_argument("mail", type=str, help="Mail of the user is required")
verify_args.add_argument("password", type=str, help="Password of the user is required")

resource_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"surname": fields.String,
	"mail": fields.String,
	"image": fields.String,
	"birthdate": fields.DateTime,
	"created_at": fields.DateTime,
	"updated_at": fields.DateTime,
	"gender_id": fields.Integer,
	"type_user_id": fields.Integer
}

class UserResource(Resource):
	@marshal_with(resource_fields)
	def get(self, user_id):
		result = User.get_by_id(user_id)

		if not result:
			abort(404, message="Could not find user with that id")

		return result, 200

	@marshal_with(resource_fields)
	def patch(self, user_id):
		args = update_args.parse_args()
		user = User.get_by_id(user_id)

		update = False

		if user is None:
			abort(409, message="User does not exists")

		if not args['name'] is None:
			update = True
			user.name = args['name']

		if not args['surname'] is None:
			update = True
			user.surname = args['surname']

		if not args['mail'] is None:
			result = User.get_by_mail(mail=args['mail'])
			if not result is None:
				abort(409, message="Mail is register already")
			update = True
			user.mail = args['mail']

		if not args['password'] is None:
			update = True
			user.un_password = args['password']

		if not args['image'] is None:
			update = True
			user.image = args['image']

		if not args['gender_id'] is None:
			gender = Gender.get_by_id(args['gender_id'])
			if gender is None:
				abort(409, message="Gender id does not exist")
			update = True
			user.gender_id = args['gender_id']

		if not args['type_user_id'] is None:
			type_user = TypeUser.get_by_id(args['type_user_id'])
			if type_user is None:
				abort(409, message="User type id does not exist")
			update = True
			user.type_user_id = args['type_user_id']

		if update:
			user.updated_at = datetime.today()

		User.create_element(user)
		return user, 201

	def delete(self, user_id):
		return {'message': 'Delete is not implemented'}, 501


class AllUserResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = User.get_all()

		if not result:
			abort(404, message="Could not find any user")

		return result, 200

	@marshal_with(resource_fields)
	def put(self):
		args = put_args.parse_args()
		result = User.get_by_mail(args['mail'])

		if result:
			abort(409, message="User mail already exists")

		gender = Gender.get_by_id(args['gender_id'])
		type_user = TypeUser.get_by_id(args['type_user_id'])

		if gender is None:
			abort(409, message="Gender id does not exist")

		if type_user is None:
			abort(409, message="User type id does not exist")		

		user = User(name=args['name'], surname=args['surname'], mail=args['mail'],
					un_password=args['password'], image=args['image'], format_date=args['birthdate'],
					gender_id=args['gender_id'], type_user_id=args['type_user_id'])

		User.create_element(user)
		return user, 201


class VerifyUserResource(Resource):
	def post(self):
		args = verify_args.parse_args()

		result = User.get_by_mail(args['mail'])

		if result is None:
			return {"response": False, "message": "The mail is incorrect"}
		else:
			pass_validate = result.verify_password(args['password'])
			
			if pass_validate:
				return {"response": True, "message": "User authenticated"}

			else:
				return {"response": False, "message": "The password is incorrect"}