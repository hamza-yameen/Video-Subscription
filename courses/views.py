from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Courses
from membership.models import UserMembership, Membership


class CourseListView(ListView):
    queryset = Courses.objects.all()
    template_name = "courses/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        return context


class CourseDetailView(DetailView):
    queryset = Courses.objects.all()
    template_name = "courses/detail.html"


class LessonView(View):

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):

        course_qs = Courses.objects.filter(slug=course_slug)
        if course_qs.exists():
            course = course_qs.first()

        lesson_qs = course.Lesson.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lessons = lesson_qs.first()

        usermembership = UserMembership.objects.filter(user=request.user).first()
        usermember_shiptype = usermembership.member_ship.membership_type
        course_allowed_mem_type = course.allowed_membership.all()

        context = {
            'object': None
        }

        if course_allowed_mem_type.filter(membership_type=usermember_shiptype).first():
            context = {
                'object': lessons
            }

        return render(request, "courses/lesson_detail.html", context)