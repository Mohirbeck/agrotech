from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe


class Address(models.Model):
    address = models.CharField(max_length=255)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    company = models.ForeignKey('Company', models.RESTRICT)

    def __str__(self):
        return self.address
    
class Document(models.Model):
    type_choices = (
        ('1', 'Price list'),
        ('2', 'Catalog'),
        ('3', 'Certificate'),
        ('4', 'Other'),
    )
    order = models.ForeignKey('Order', on_delete=models.RESTRICT)
    file = models.FileField(upload_to='documents')
    type = models.CharField(max_length=50, choices=type_choices, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.type == '1':
            return 'Price list'
        elif self.type == '2':
            return 'Catalog'
        elif self.type == '3':
            return 'Certificate'
        elif self.type == '4':
            return 'Other'
        else:
            return 'Other'


role_choices = (
    ('1', 'Farmer'),
    ('2', 'HoReCa'),
    ('3', 'Manufacturer'),
)

class Company(models.Model):

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='companies', null=True, blank=True)
    role = models.CharField(max_length=50, choices=role_choices, default='1')

    def __str__(self):
        return self.name


class FavoriteProducts(models.Model):
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class CustomUserManager(BaseUserManager):
    '''
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    '''
    def create_user(self, email, password, **extra_fields):
        '''
        Create and save a user with the given email and password.
        '''
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        '''
        Create and save a SuperUser with the given email and password.
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    filter = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='categories')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    layer = models.IntegerField(default=0)
    is_last = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_full_url(self):
        return 'https://nt-techonosoft.uz' + self.image.url


    def __str__(self):
        return self.name
    
class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    status_choices = (
        ('1', 'Active'),
        ('2', 'Inactive'),
        ('3', 'Deleted')
    )
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='products')
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(null=True, blank=True)
    features = models.JSONField(null=True, blank=True)
    stock = models.IntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    status = models.CharField(max_length=50, choices=status_choices, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    

class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_quantity = models.IntegerField()
    max_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    

class CartProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.RESTRICT, related_name='Cats')
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField(default=1)
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE, related_name='cart_products')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='cart_products')
    description = models.TextField(null=True, blank=True)
    features = models.JSONField(null=True, blank=True)
    stock = models.IntegerField(default=0)
    
    price = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SetGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class Cart(models.Model):
    
    class Status(models.TextChoices):
        ACTIVE = 'active'
        SET = 'set'
        ARCHIVED = 'archived'

    set_goup = models.ForeignKey(SetGroup, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE, null=True, blank=True)
    cart_status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    quantity = models.IntegerField(default=1)
    comment = models.TextField(null=True, blank=True)
    cart_product = models.ForeignKey(CartProduct, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f'{self.user.email} - {self.product.name}'


class Order(models.Model):
    status_choices = (
        ('1', 'New'),
        ('2', 'In progress'),
        ('3', 'Completed'),
    )
    payment_status_choices = (
        ('1', 'Not paid'),
        ('2', 'Paid'),
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=status_choices, default='1')
    payment_status = models.CharField(max_length=50, choices=payment_status_choices, default='1')
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.created_at}'


class EmailCode(models.Model):
    email = models.CharField(max_length=50, db_index=True)
    ip = models.GenericIPAddressField(db_index=True)
    code = models.CharField(max_length=10)
    expire_at = models.DateTimeField(db_index=True)

    class Meta:
        index_together = []


class EmailAttempt(models.Model):
    email = models.CharField(max_length=50, db_index=True)
    counter = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(db_index=True)


class Application(models.Model):
    STATUS = (
        (1, 'Waiting'),
        (2, 'Accepted')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    name_company = models.CharField(max_length=255)
    type_company = models.CharField(max_length=50, choices=role_choices, default='1')
    contact = models.CharField(max_length=25)
    inn = models.CharField(max_length=20)
    email_company = models.EmailField(_('email address'), unique=True)
    owner_name = models.CharField(max_length=50)
    owner_email = models.EmailField(_('email address'), unique=True)
    owner_phone = models.CharField(max_length=50)

    def approve(self):
        return mark_safe(f'<a href="/approve/{self.id}" height="150">approve<a/>')