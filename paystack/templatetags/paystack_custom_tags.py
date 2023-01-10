# # from course.models import UserCourse, Course
# from paystack.models import CustomerInfo
from django import template

register = template.Library()  # register the template tag

# @register.simple_tag
# def is_enrolled(request, course):
#     user = None
#     if not request.user.is_authenticated:
#         return False
#         # i you are enrooled in this course you can watch every video
#     user = request.user
#     try:
#         user_course = UserCourse.objects.get(user=user, course=course)
#         return True
#     except:
#         return False
