from django.contrib import admin
from classes.models import FitnessClass, ClassBooking, Attendance, Feedback

admin.site.register(FitnessClass)
admin.site.register(ClassBooking)
admin.site.register(Attendance)
admin.site.register(Feedback)

# Register your models here.
