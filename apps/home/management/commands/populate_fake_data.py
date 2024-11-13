from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from apps.home.models import Employee, KPI, PerformanceReview, ReviewCycle, Feedback

class Command(BaseCommand):
    help = 'Populate fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Loop to create 25 records
        for _ in range(25):
            # Create a fake user
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',  # Set a default password
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            # Create Employee with the created User
            employee = Employee.objects.create(
                user=user,  # Assign the created User instance here
                department=fake.word(),
                position=fake.job(),
                date_joined=fake.date_this_decade(),
            )

            # Create KPI
            kpi = KPI.objects.create(
                name=fake.bs(),
                description=fake.text(),
                target_value=fake.random_number(),
                unit=fake.word(),
            )

            # Create ReviewCycle
            review_cycle = ReviewCycle.objects.create(
                name=fake.word(),
                start_date=fake.date_this_year(),
                end_date=fake.date_this_year(),
            )

            # Create PerformanceReview
            performance_review = PerformanceReview.objects.create(
                employee=employee,
                kpi=kpi,
                review_cycle=review_cycle,
                achieved_value=fake.random_number(),
            )

            # Create Feedback
            feedback = Feedback.objects.create(
                performance_review=performance_review,
                comments=fake.text(),
            )

        # Print success message
        self.stdout.write(self.style.SUCCESS('Successfully populated 25 fake data records!'))
