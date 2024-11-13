from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Employee
from .forms import UserCreationForm, EmloyeeCreationForm
from django.contrib import messages
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
    
    return render(request, 'home/tables.html', context)


@login_required(login_url="/login/")
def add_user(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        employee_form = EmloyeeCreationForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            messages.sucess(request,"User Added sucessfully")
            return redirect('employee')
        else:
            messages.error(request,"There was an error in the form Submission")
    else:
        user_form = UserCreationForm()
        employee_form = EmloyeeCreationForm()
    context = {
        'user_form':user_form,
        'employee_form':employee_form
    }
    return render (request,'home/add_user.html',context)
        


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
