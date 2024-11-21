from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from collections import defaultdict
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Employee, KPI,ReviewCycle,PerformanceReview,User
from .forms import UserCreationForm, EmployeeCreationForm, KPICreationForm, ReviewCycleForm,PerformanceReviewForm
from django.contrib import messages
from django.db.models import Avg
@login_required(login_url="/login/")
def index(request):
    # Render the 'home/index.html' template with context
    context = {'segment': 'index'}
    return render(request, 'home/index.html', context)

@login_required(login_url="/login/")
def employee(request):
    # Retrieve all employees from the database
    employee_list = Employee.objects.all()
    
    # Set the number of employees to display per page
    paginator = Paginator(employee_list, 10)  # 10 employees per page
    
    # Get the page number from the request
    page_number = request.GET.get('page')
    
    # Get the employees for the current page
    page_obj = paginator.get_page(page_number)

    # Pass the paginated results to the template
    context = {
        'employees': page_obj,
        'segment': 'employee',  # Add 'employee' to segment context for active link
    }
    
    return render(request, 'home/employee.html', context)

@login_required(login_url="/login/")
def add_user(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        employee_form = EmployeeCreationForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid():
            # Save user
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            print("User saved:", user.username)

            # Save employee
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            print("Employee saved:", employee)

            messages.success(request, "User and Employee successfully added.")
            return redirect('employee')
        else:
            print("User form errors:", user_form.errors)
            print("Employee form errors:", employee_form.errors)
            messages.error(request, "Error in form submission. Please correct the errors.")

    else:
        user_form = UserCreationForm()
        employee_form = EmployeeCreationForm()

    context = {
        'user_form': user_form,
        'employee_form': employee_form,
    }
    return render(request, 'home/add_user.html', context)



@login_required(login_url="/login/")
def kpi(request):
    # Retrieve all employees from the database
    kpi_list = KPI.objects.all()
    
    paginator = Paginator(kpi_list, 10)  
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'kpis': page_obj,
        'segment': 'kpi',
    }
    
    return render(request, 'home/kpi.html', context)

@login_required(login_url="/login/")
def add_kpi(request):
    if request.method == 'POST':
        kpi_form = KPICreationForm(request.POST)
        if kpi_form.is_valid():
            kpi = kpi_form.save(commit=False)
            kpi.save()
            messages.success(request, "KPI successfully added.")
            return redirect('kpi')
        else:
            messages.error(request, "Error in form submission. Please correct the errors.")
    else:
        kpi_form = KPICreationForm()

    context = {
        'kpi_form': kpi_form,
    }    
    return render(request, 'home/add_kpi.html', context)

@login_required(login_url="/login/")
def review_cycle(request):
    # Retrieve all review cycles from the database
    review_cycle_list = ReviewCycle.objects.all()
    
    paginator = Paginator(review_cycle_list, 10)  # Paginate with 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'review_cycles': page_obj,
        'segment': 'review_cycle',  # Set segment for highlighting menu
    }
    
    return render(request, 'home/review_cycle.html', context)


@login_required(login_url="/login/")
def add_review_cycle(request):
    if request.method == 'POST':
        review_cycle_form = ReviewCycleForm(request.POST)
        if review_cycle_form.is_valid():
            review_cycle = review_cycle_form.save(commit=False)
            review_cycle.save()
            messages.success(request, "Review Cycle successfully added.")
            return redirect('review_cycle')
        else:
            messages.error(request, "Error in form submission. Please correct the errors.")
    else:
        review_cycle_form = ReviewCycleForm()

    context = {
        'review_cycle_form': review_cycle_form,
    }    
    return render(request, 'home/add_review_cycle.html', context)




@login_required(login_url="/login/")
def performance_reviews(request):
    reviews = PerformanceReview.objects.select_related('employee', 'kpi', 'review_cycle').all()
    context = {
        'reviews': reviews
    }
    return render(request, 'home/preview.html', context)

@login_required(login_url="/login/")
def add_performance_review(request):
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Performance review added successfully.")
            return redirect('performance_reviews')
        else:
            messages.error(request, "Error adding performance review.")
    else:
        form = PerformanceReviewForm()

    context = {'form': form}
    return render(request, 'home/add_preview.html', context)





@login_required(login_url="/login/")
def pages(request):
    context = {}
    # Extract the template name from the URL path
    load_template = request.path.split('/')[-1]
    
    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))

    try:
        context['segment'] = load_template
        # Render the template dynamically based on the URL
        return render(request, f'home/{load_template}', context)

    except template.TemplateDoesNotExist:
        # Return 404 page if the template does not exist
        return render(request, 'home/page-404.html', context)

    except Exception:
        # Return 500 page for any other errors
        return render(request, 'home/page-500.html', context)
    

def kpi_completion_all_users(request):
    # Initialize the result dictionary
    result = {}

    # Get all employees
    employees = Employee.objects.all()

    # Loop through each employee and collect KPI completion data
    for employee in employees:
        # Get performance reviews for the employee
        reviews = PerformanceReview.objects.filter(employee=employee)
        
        # Prepare the cycle labels (assuming they are the same for all employees)
        cycle_labels = list(ReviewCycle.objects.all().values_list('name', flat=True))

        # Prepare the KPI trend data for the employee
        kpi_trend = []
        for cycle in cycle_labels:
            cycle_reviews = reviews.filter(review_cycle__name=cycle)
            for review in cycle_reviews:
                kpi_trend.append(review.achieved_value)  # KPI completion value for that cycle

        # Add the employee's data to the result
        result[employee.user.username] = {
            'cycle_labels': cycle_labels,
            'kpi_trend': kpi_trend
        }

    # Return the result as JSON
    return JsonResponse(result)


def employee_kpi_performance(request):
    # Initialize the result dictionary
    result = defaultdict(lambda: defaultdict(list))

    # Get all employees
    employees = Employee.objects.all()

    # Loop through each employee and collect KPI performance data
    for employee in employees:
        # Get performance reviews for the employee
        reviews = PerformanceReview.objects.filter(employee=employee)

        # Prepare the cycle labels (assuming they are the same for all employees)
        cycle_labels = list(ReviewCycle.objects.all().values_list('name', flat=True))

        # Prepare the KPI performance data for the employee
        for cycle in cycle_labels:
            cycle_reviews = reviews.filter(review_cycle__name=cycle)
            for review in cycle_reviews:
                # Aggregate achieved_value by KPI for each cycle
                result[employee.user.username][cycle].append({
                    'kpi_name': review.kpi.name,
                    'achieved_value': review.achieved_value,
                    'target_value': review.kpi.target_value
                })

    # Convert defaultdict to a regular dict before returning the response
    result = dict(result)

    return JsonResponse(result)

def employee_performance_trend(request):
    result = {}

    # Get all employees
    employees = Employee.objects.all()

    # Loop through each employee to get their performance trend
    for employee in employees:
        # Get all performance reviews for this employee
        reviews = PerformanceReview.objects.filter(employee=employee).select_related('review_cycle')

        # Prepare the cycle labels (assuming cycles are ordered)
        cycle_labels = list(ReviewCycle.objects.all().values_list('name', flat=True))

        # Prepare the trend data for the employee
        performance_trend = []
        for cycle in cycle_labels:
            # Filter the reviews for the current cycle
            cycle_reviews = reviews.filter(review_cycle__name=cycle)
            if cycle_reviews.exists():
                # Get the achieved_value for the most recent review in this cycle
                performance_trend.append(cycle_reviews.first().achieved_value)
            else:
                # If no review exists for the cycle, append a default value (e.g., 0)
                performance_trend.append(0)

        # Store the data for this employee
        result[employee.user.username] = {
            'cycle_labels': cycle_labels,
            'performance_trend': performance_trend
        }

    return JsonResponse(result)