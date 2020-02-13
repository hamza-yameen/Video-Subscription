from django.db import models
from membership.models import Membership
from django.urls import reverse


# Create your models here.
class Courses(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_membership = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    @property
    def Lesson(self):
        return self.lesson_set.all().order_by('position')


class lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    thumnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:listdetail", kwargs={"course_slug": self.course.slug, "lesson_slug": self.slug})
