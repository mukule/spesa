from django.db import models
from users.models import *


class Hero(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to='panel_images/', default='default/hero.png')

    def __str__(self):
        return self.title


class Risk(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(
        upload_to='risks_icons/', default='default/icon.png')

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(
        upload_to='speciality_icons/', default='default/default_icon.png')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class FinancialConcern(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    banner = models.ImageField(
        upload_to='financial_concern_banners/', default='default/banner.png')

    def __str__(self):
        return self.name


class About(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='about_icons/',
                             default='default/about_icon.png')

    def __str__(self):
        return self.name


class Panel(models.Model):
    name = models.CharField(max_length=100)
    title = models.TextField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to='panel_images/', default='default/panel.png')

    def __str__(self):
        return self.name


class Works(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    banner = models.ImageField(
        upload_to='blog_banners/', default='default/blog.png')
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.name}"


class Consult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    handler = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                blank=True, related_name='handled_consults', limit_choices_to={'access_level': 2})
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checkout_request_id = models.CharField(
        max_length=100, null=True, blank=True)
    transaction_code = models.CharField(max_length=100, null=True, blank=True)
    assigned = models.BooleanField(default=False)
    payment_confirmation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0

                                     )
    task_accepted = models.BooleanField(default=False)
    task_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s {self.category} Consult"


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_code = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    package = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment for {self.user.username} - {self.amount} for {self.package}"


class TempConsultation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_id = models.IntegerField()
    amount = models.FloatField()
    phone = models.CharField(max_length=15)
    checkout_request_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


class ConsultantPercentage(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.amount}%"


class Commission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE,
                                related_name='commission_consults')  # Updated related_name
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.consult.category} - {self.date_created}"


class Response(models.Model):
    consult = models.ForeignKey(
        'Consult',
        on_delete=models.CASCADE,
        related_name='responses'
    )
    accepted = models.BooleanField(default=False)
    admin_response = models.TextField()
    satisfied = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)
    response_doc = models.FileField(
        upload_to='response_docs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    more_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Response for {self.consult}"


class Section1(models.Model):
    name = models.CharField(max_length=100)
    tag1 = models.CharField(max_length=300)
    tag2 = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Section2(models.Model):
    name = models.CharField(max_length=100)
    tag1 = models.CharField(max_length=300)
    tag2 = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class How(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Spesa(models.Model):

    description = models.TextField()

    def __str__(self):
        return self.description


class Ad(models.Model):

    description = models.TextField()

    def __str__(self):
        return self.description


class Terms(models.Model):

    descriptions = models.TextField()

    def __str__(self):
        return self.descriptions
