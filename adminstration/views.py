from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import *
from users.models import *
from main.models import *
from .forms import *
from django.db.models import Count
from django.http import Http404
from django.utils import timezone

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
    context = {
        'users': users,
        'specialities': specialities,
        'f_concerns': financial_concern,
        'abouts': abouts,
        'panel': panel,
        'works': works,
        'categories': categories
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

        return render(request, 'adminstration:admin', {'error_message': 'You cannot create more than 3 About instances.'})

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
