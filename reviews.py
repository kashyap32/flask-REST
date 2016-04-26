from flask.ext.restful import Resource,Api,reqparse,inputs,fields,marshal,marshal_with

from flask import Blueprint,url_for,abort
import models



review_fields={
    'id':fields.Integer,
    'rating': fields.Integer,
    'comment':fields.String,
   # 'created_at':fields.DateTime

}
def review_or_404(review_id):
    try:
        review = models.Review.get(models.Review.id==review_id)
    except models.Review.DoesNotExist:
        abort(404)
    else:
        return review
def add_course(review):

    review.for_course=url_for('courses.course',id=review.course.id)
    return review
class Reviewlist(Resource):
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument(
            'course',
            type=inputs.positive,
            required=True,
            help="NO  course provided",
            location=['Form','json']
        )
        self.reqparse.add_argument(
            'rating',
            required=True,
            type=inputs.int_range(1,5),
            help="NO rating  provided",
            location=['Form','json'],

        )
        self.reqparse.add_argument(
            'comment',
            required=False,
            nullable=True,
            help="NO comment  provided",


        )
        super(Reviewlist,self).__init__()

    def get(self):

        reviews= [marshal(add_course(reviews), review_fields)for reviews in models.Review.select()]
        return {'review':reviews}
    @marshal_with(review_fields)
    def post(self):
        args=self.reqparse.parse_args()
        review=models.Review.create(**args)
        return add_course(review)

class Review(Resource):
    @marshal_with(review_fields)
    def get(self,id):
        return add_course(review_or_404(id))
    def put(self,id):
        return ''
    def delete(self,id):
        return ''
reviews_api=Blueprint('reviews',__name__)

api=Api(reviews_api)
api.add_resource(
    Reviewlist,
    '/api/v1/reviews',
    endpoint='reviews'


)
api.add_resource(
    Review,
    '/api/v1/reviews/<int:id>',
    endpoint='review'

)