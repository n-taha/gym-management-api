from django.db import models
from users.models import User
import datetime
class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes', limit_choices_to={'role':'STAFF'})
    description = models.TextField()
    schedule_date = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class ClassBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'fitness_class']]

    def __str__(self):
        return f"{self.user.first_name} → {self.fitness_class.name}"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendence')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='attendence')
    date = models.DateField(default=datetime.date.today())
    attended = models.BooleanField(default=False)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'fitness_class', 'date']]

    def __str__(self):
        return f"{self.user.first_name} - {self.fitness_class.name}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.rating}"
