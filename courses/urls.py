from django.urls import path
from .views import CourseListView, CourseDetailView, LessonView

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('<slug>', CourseDetailView.as_view(), name='detail'),
    path('<course_slug>/<lesson_slug>', LessonView.as_view(), name='listdetail')
]