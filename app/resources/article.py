from flask_restful import Resource, reqparse, abort, fields, marshal_with
from ..models import Article


put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="Name of the article is required", required=True)
put_args.add_argument("content", type=str, help="Content of the article is required", required=True)
put_args.add_argument("section_id", type=int, help="Section id of the article is required", required=True)

"""
class Comments(fields.Raw):
	def format(self, value):
		comments = []
		for val in value:
			comment = CommentResource.get(val.id)
			comments.append(comment)
		return comments
"""

resource_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"content": fields.String,
	"section_id": fields.Integer,
	#"comments": Comments,
	#"progress": Progress,
}


class ArticleResource(Resource):
	@classmethod
	@marshal_with(resource_fields)
	def get(self, article_id):
		result = Article.get_by_id(article_id)

		if not result:
			abort(404, message="Could not find an article with that id")

		return result

	@marshal_with(resource_fields)
	def update(self, article_id):
		pass


class AllArticleResource(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Article.get_all()

		if not result:
			abort(404, message="Could not find any article")

		return result

	@marshal_with(resource_fields)
	def put(self):
		args = put_args.parse_args()

		section = Section.get_by_id(args['section_id'])

		if section is None:
			abort(409, message="Section id does not exists")

		article = Article(name=args['name'], content=args['content'],
							course_id=args['section_id'])

		Article.create_element(article)
		return article, 201