from django.contrib import admin
from .models import Address, Document, Company, Position, User, Product, ProductImage, ProductPrice, Cart, Order, UnitOfMeasure, Category, Article, Application


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'longitude', 'latitude']
    list_display_links = ['id', 'address']
    search_fields = ['address']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'type', 'created_at', 'updated_at']
    list_display_links = ['id', 'file']
    search_fields = ['type']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'role']
    list_display_links = ['id', 'name']
    search_fields = ['name']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'company', 'position']
    list_display_links = ['id', 'email']
    search_fields = ['email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'company']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    inlines = [ProductImageInline, ProductPriceInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_display_links = ['id', 'user']
    search_fields = ['user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status']
    list_display_links = ['id', 'user']
    search_fields = ['user']

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    search_fields = ['name']


@admin.register(Application)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_company', 'owner_name', 'contact']
    list_display_links = ['id', 'name_company']
    search_fields = ['name_company']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']
    list_display_links = ['id', 'product']
    # search_fields = ['name_company']s

    