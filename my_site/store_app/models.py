from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    STATUS_CHOICES = (
        ('gold', 'gold'),
        ('silver', 'silver'),
        ('bronze', 'bronze'),
        ('simple', 'simple'),
    )
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(70)],
                                            null=True, blank=True)

    phone_model = PhoneNumberField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='simple')
    date_register = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Category(models.Model):
    Category_name = models.CharField(max_length=32, unique=True)
    Category_image = models.ImageField(upload_to='photo_category/')

    def __str__(self):
        return self.Category_name


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=32, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_sub')

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategory_product')
    description = models.TextField()
    product_type = models.BooleanField(default=False, null=True, blank=True)
    article = models.PositiveIntegerField(unique=True)
    video = models.FileField(null=True, blank=True)
    created_data = models.DateField(auto_now_add=True)

    def get_average_rating(self):
        ratings = self.product_review.all()
        if ratings.exists():
            return sum(i.star for i in ratings) / ratings.count()
        return 0

    def get_count_people(self):
        ratings = self.product_review.all()
        if ratings.exists():
            return ratings.count()
        return 0

    def __str__(self):
        return f'{self.product_name}, {self.price}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photo_product')
    product_image = models.ImageField(upload_to='image_product/')

    def __str__(self):
        return self.product.product_name


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    star = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)],
                                             null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.star}★'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def get_total_price(self):
        return sum([i.get_total_price() for i in self.items.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price