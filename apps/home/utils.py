from django.db.models import F
from .models import PerformanceReview, KPI, ReviewCycle

def calculate_all_kpi_performance():
    performance_data = {}

    # Fetch all review cycles
    review_cycles = ReviewCycle.objects.all()

    for review_cycle in review_cycles:
        performance_data[review_cycle.name] = {}

        # Fetch all KPIs
        kpis = KPI.objects.all()

        for kpi in kpis:
            # Get all performance reviews for the given cycle and KPI
            performance_reviews = PerformanceReview.objects.filter(
                review_cycle=review_cycle,
                kpi=kpi
            )

            total_employees = performance_reviews.count()

            # If no reviews, skip to next KPI
            if total_employees == 0:
                continue

            exceeded = performance_reviews.filter(achieved_value__gt=F('kpi__target_value')).count()
            met = performance_reviews.filter(achieved_value=F('kpi__target_value')).count()
            underperformed = performance_reviews.filter(achieved_value__lt=F('kpi__target_value')).count()

            # Calculate the percentages
            exceeded_percentage = (exceeded / total_employees) * 100
            met_percentage = (met / total_employees) * 100
            underperformed_percentage = (underperformed / total_employees) * 100

            performance_data[review_cycle.name][kpi.name] = {
                'exceeded': exceeded_percentage,
                'met': met_percentage,
                'underperformed': underperformed_percentage
            }

    return performance_data