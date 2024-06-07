from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import *
from users.models import *
from main.models import *
from .forms import *
from django.db.models import Count
from django.http import Http404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Create your views here.


@admin
def dashboard(request):
    users = CustomUser.objects.filter(access_level__in=[2, 3])
    specialities = Speciality.objects.all()
    financial_concern = FinancialConcern.objects.all()
    abouts = About.objects.all()
    panel = Panel.objects.all()
    works = Works.objects.all()
    categories = Category.objects.annotate(num_blogs=Count('blog'))

    # Retrieve all consults and order them by id in descending order
    consults = Consult.objects.all().order_by('-id')

    try:
        hero_instance = Hero.objects.get(pk=1)
    except Hero.DoesNotExist:
        hero_instance = None

    # Paginate the consults to display 10 per page
    paginator = Paginator(consults, 10)

    page_number = request.GET.get('page')
    try:
        consults = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        consults = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        consults = paginator.page(paginator.num_pages)

    context = {
        'users': users,
        'specialities': specialities,
        'f_concerns': financial_concern,
        'abouts': abouts,
        'panel': panel,
        'works': works,
        'categories': categories,
        'consults': consults,
        'hero': hero_instance,
    }
    return render(request, 'adminstration/dashboard.html', context)


@admin
def create_speciality(request):
    if request.method == 'POST':
        form = SpecialityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a success page or URL
            return redirect('adminstration:admin')
    else:
        form = SpecialityForm()
    return render(request, 'adminstration/create_speciality.html', {'form': form})


@admin
def edit_speciality(request, speciality_id):
    speciality = get_object_or_404(Speciality, id=speciality_id)
    if request.method == 'POST':
        form = SpecialityForm(request.POST, request.FILES, instance=speciality)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = SpecialityForm(instance=speciality)
    return render(request, 'adminstration/edit_speciality.html', {'form': form, 'speciality': speciality})


@admin
def delete_speciality(request, speciality_id):
    speciality = get_object_or_404(Speciality, id=speciality_id)

    speciality.delete()
    return redirect('adminstration:admin')


@admin
def create_financial_concern(request):
    if request.method == 'POST':
        form = FinancialConcernForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a success page or URL
            return redirect('adminstration:admin')
    else:
        form = FinancialConcernForm()
    return render(request, 'adminstration/create_financial_concern.html', {'form': form})


@admin
def edit_financial_concern(request, concern_id):
    concern = get_object_or_404(FinancialConcern, id=concern_id)
    if request.method == 'POST':
        form = FinancialConcernForm(
            request.POST, request.FILES, instance=concern)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = FinancialConcernForm(instance=concern)
    return render(request, 'adminstration/edit_financial_concern.html', {'form': form, 'concern': concern})


@admin
def delete_financial_concern(request, concern_id):
    concern = get_object_or_404(FinancialConcern, id=concern_id)

    concern.delete()

    return redirect('adminstration:admin')


@admin
def create_about(request):
    if About.objects.count() >= 3:

        messages.error(
            request, "You can not Create more than 3")

        return redirect('adminstration:admin',)

    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = AboutForm()
    return render(request, 'adminstration/create_about.html', {'form': form})


@admin
def edit_about(request, about_id):
    about_instance = get_object_or_404(About, id=about_id)
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=about_instance)
        if form.is_valid():
            form.save()

            return redirect('adminstration:admin')
    else:
        form = AboutForm(instance=about_instance)
    return render(request, 'adminstration/edit_about.html', {'form': form, 'about': about_instance})


@admin
def delete_about(request, about_id):
    about_instance = get_object_or_404(About, id=about_id)

    about_instance.delete()

    return redirect('adminstration:admin')


@admin
def create_panel(request):
    existing_panel = Panel.objects.first()
    if existing_panel:
        return redirect('adminstration:admin')

    if request.method == 'POST':
        form = PanelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = PanelForm()
    return render(request, 'adminstration/create_panel.html', {'form': form})


@admin
def edit_panel(request, panel_id):
    panel_instance = get_object_or_404(Panel, id=panel_id)

    if request.method == 'POST':
        form = PanelForm(request.POST, request.FILES, instance=panel_instance)
        if form.is_valid():
            form.save()

            return redirect('adminstration:admin')
    else:
        form = PanelForm(instance=panel_instance)

    return render(request, 'adminstration/edit_panel.html', {'form': form, 'panel_instance': panel_instance})


@admin
def delete_panel(request, panel_id):
    panel_instance = get_object_or_404(Panel, id=panel_id)
    panel_instance.delete()
    return redirect('adminstration:admin')


@admin
def create_works(request):
    if request.method == 'POST':
        form = WorksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = WorksForm()
    return render(request, 'adminstration/create_works.html', {'form': form})


@admin
def edit_works(request, works_id):
    works_instance = get_object_or_404(Works, id=works_id)
    if request.method == 'POST':
        form = WorksForm(request.POST, instance=works_instance)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = WorksForm(instance=works_instance)
    return render(request, 'adminstration/edit_works.html', {'form': form, 'work': works_instance})


@admin
def delete_works(request, works_id):
    works_instance = get_object_or_404(Works, id=works_id)

    works_instance.delete()
    return redirect('adminstration:admin')


@admin
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = CategoryForm()
    return render(request, 'adminstration/create_category.html', {'form': form})


@admin
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'adminstration/edit_category.html', {'form': form})


@admin
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    category.delete()
    return redirect('adminstration:admin')


@admin
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    blogs = Blog.objects.filter(category=category)
    context = {'category': category, 'blogs': blogs}
    return render(request, 'adminstration/category_detail.html', context)


@admin
def create_blog(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.category = category
            blog.created_by = request.user
            blog.created_at = timezone.now()
            blog.save()
            return redirect('adminstration:admin')
    else:
        form = BlogForm(initial={'category': category})
    return render(request, 'adminstration/create_blog.html', {'form': form})


@admin
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        # Assuming BlogForm includes the category field
        form = BlogForm(instance=blog)
    return render(request, 'adminstration/edit_blog.html', {'form': form})


@admin
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    blog.delete()
    return redirect('adminstration:admin')


@admin
def assign_handler_view(request, consult_id):
    consult = get_object_or_404(Consult, id=consult_id)
    rate = ConsultantPercentage.objects.first()

    if not consult.payment_confirmation:
        messages.error(
            request, "Payment confirmation is required before assigning a handler.")
        return redirect('adminstration:admin')

    if request.method == 'POST':
        form = AssignHandlerForm(request.POST, instance=consult)
        if form.is_valid():
            # Save the form which updates the handler
            form.save()

            # Update commission based on Consultant Percentage
            if rate:
                commission = consult.price * (rate.amount / 100)
            else:
                # If Consultant Percentage is not set, default commission to 30% of the consult price
                commission = consult.price * 0.3

            # Update commission in the Consult model
            consult.commission = commission
            consult.save()

            messages.success(
                request, f"Handler assigned to {consult.category} consult.")
            return redirect('adminstration:admin')
    else:
        initial_data = {
            'handler': consult.handler_id} if consult.handler else None
        form = AssignHandlerForm(instance=consult, initial=initial_data)

    # Update commission based on Consultant Percentage
    if rate:
        commission = consult.price * (rate.amount / 100)
    else:
        # If Consultant Percentage is not set, default commission to 30% of the consult price
        commission = consult.price * 0.3

    return render(request, 'adminstration/assign_handler.html', {'form': form, 'consult': consult, 'rate': rate, 'commission': commission})


@admin
def create_or_update_consultant_percentage(request):
    try:
        consultant_percentage = ConsultantPercentage.objects.get()
    except ConsultantPercentage.DoesNotExist:
        consultant_percentage = None

    if request.method == 'POST':
        form = ConsultantPercentageForm(
            request.POST, instance=consultant_percentage)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            if amount < 0:
                form.add_error('amount', 'Percentage cannot be negative.')
            elif amount > 100:
                form.add_error('amount', 'Percentage cannot exceed 100.')
            else:
                form.save()
                messages.success(
                    request, 'Consultant percentage Updated succesfully')
                return redirect('adminstration:consultant_percentage')
    else:
        form = ConsultantPercentageForm(instance=consultant_percentage)

    return render(request, 'adminstration/create_consultant_percentage.html', {'form': form})


@login_required
def update_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    if request.method == 'POST':
        form = AdminResponseForm(request.POST, instance=response)
        if form.is_valid():
            form.save()
            return redirect('main:response_detail', response_id=response_id)
    else:
        form = AdminResponseForm(instance=response)

    return render(request, 'adminstration/update_response.html', {'form': form, 'response': response})


@login_required
def update_hero(request):
    try:
        instance = Hero.objects.get(pk=1)
    except Hero.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('adminstration:admin')
    else:
        form = HeroForm(instance=instance)

    return render(request, 'adminstration/create_hero.html', {'form': form})


@login_required
def hero(request):
    try:
        hero_instance = Hero.objects.get(pk=1)
    except Hero.DoesNotExist:
        hero_instance = None

    return render(request, 'adminstration/hero.html', {'hero': hero_instance})
