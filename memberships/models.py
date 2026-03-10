from django.db import models
from users.models import User

# Create your models here.
class MembershipPlan(models.Model):
    PLAN_DURATION = (
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )

    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=10, choices=PLAN_DURATION)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.plan.name}"

