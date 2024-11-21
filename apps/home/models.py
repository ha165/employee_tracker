from django.contrib.auth.models import User
from django.db import models

#employee model extending the django defaults model
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Connect to Django's user model
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

#Kpi model
class KPI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    target_value = models.FloatField()  # Target value for achieving this KPI
    unit = models.CharField(max_length=50)  # E.g., 'percentage', 'tasks', etc.

    def __str__(self):
        return self.name

#review cycle model
class ReviewCycle(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

#perfomance review
class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    review_cycle = models.ForeignKey(ReviewCycle, on_delete=models.CASCADE)
    achieved_value = models.FloatField()  # Value achieved in this cycle

    def __str__(self):
        return f"{self.employee} - {self.kpi} ({self.review_cycle})"


#feedback
class Feedback(models.Model):
    performance_review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE)
    comments = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.performance_review}"
