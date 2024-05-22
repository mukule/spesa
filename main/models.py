from django.db import models
from users.models import *


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
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_code = models.CharField(
        max_length=100, blank=True, null=True)

    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Assigned'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    PAYMENT_CONFIRMATION_CHOICES = [
        (0, 'Pending'),
        (1, 'Confirmed'),
    ]
    payment_confirmation = models.CharField(
        max_length=10, choices=PAYMENT_CONFIRMATION_CHOICES, default='Pending')

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
