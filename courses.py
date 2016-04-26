from flask.ext.restful import Resource,Api,reqparse,inputs,fields,marshal,marshal_with

from flask import Blueprint,url_for,abort
import models

courses_fields={
    'id':fields.Integer,
    'title':fields.String,
    'url': fields.String,
    'reviews':fields.List(fields.String)

}


def add_reviews(course):
    course.reviews=[url_for('reviews.review',id=review.id) for review in course.review_set]
    return course
def course_404(course_id):
    try:
        course=models.Course.get(models.Course.id==course_id)
    except models.Course.DoesNotExist:
        abort(404)#message="Course {} does not Exist"
    else:
        return course


class Courselist(Resource):
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help="NO course title provided",
            location=['Form','json']
        )
        self.reqparse.add_argument(
            'url',
            required=True,
            help="NO url  provided",
            location=['Form','json'],
            type=inputs.url

        )
        super(Courselist,self).__init__()

    def get(self):
        courses=[marshal(add_reviews(courses),courses_fields)for courses in models.Course.select()]
        return {'courses':courses}

    def post(self):
        args=self.reqparse.parse_args()
        models.Course.create(**args)
        return "great"




class Course(Resource):
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help="NO course title provided",
            location=['Form','json']
        )
        self.reqparse.add_argument(
            'url',
            required=True,
            help="NO url  provided",
            location=['Form','json'],
            type=inputs.url

        )
        super(Course,self).__init__()
    @marshal_with(courses_fields)
    def get(self,id):
        return add_reviews(course_404(id))
    @marshal_with(courses_fields)
    def put(self,id):
        args=self.reqparse.parse_args()
        query=models.Course.update(**args).where(models.Course.id==id)
        query.execute()
        return (add_reviews(models.Course.get(models.Course.id==id)),200,
                {'Location':url_for('courses.course',id=id)})
    def delete(self,id):
        query=models.Course.delete().where(models.Course.id==id)
        query.execute()
        return ('deleted',200,
                {'Location':url_for('courses.courses')})

courses_api=Blueprint('courses',__name__)

api=Api(courses_api)
api.add_resource(
    Courselist,
    '/api/v1/courses',
    endpoint='courses'


)
api.add_resource(
    Course,
    '/api/v1/courses/<int:id>',
    endpoint='course'

)