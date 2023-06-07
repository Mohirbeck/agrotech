import graphene
from graphene_django import DjangoObjectType
from .models import (
    Order,
    User,
    Product,
    ProductImage,
    ProductPrice,
    UnitOfMeasure,
    Position,
    Address,
    Article,
    Document,
    Company,
    Cart,
    Category,
    Application
)

class ProductImageNode(DjangoObjectType):

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'created_at', 'updated_at')

class CompanyNode(DjangoObjectType):

    class Meta:
        model = Company
        fields = '__all__'

class UnitOfMeasureNode(DjangoObjectType):

    class Meta:
        model = UnitOfMeasure
        fields = '__all__'

class ArticleNode(DjangoObjectType):

    class Meta:
        model = Article
        fields = '__all__'

class CategoryNode(DjangoObjectType):

    class Meta:
        model = Category
        fields = '__all__'


class ProductNode(DjangoObjectType):

    class Meta:
        model = Product
        fields = '__all__'


class ApplicationNode(DjangoObjectType):

    class Meta:
        model = Application
        fields = '__all__'


class Query(graphene.ObjectType):

    application_list = graphene.List(ApplicationNode)
    application_by_id = graphene.Field(ApplicationNode, id=graphene.String())

    product_list = graphene.List(ProductNode)
    product_by_id = graphene.Field(ProductNode, id=graphene.String())
    product_image_list = graphene.List(ProductImageNode, product_id=graphene.String())
    
    category_list = graphene.List(CategoryNode)
    category_by_id = graphene.Field(CategoryNode, id=graphene.String())

    def resolve_category_list(root, info):
        return Category.objects.all()
    def resolve_category_by_id(root, info, id):
        return Category.objects.get(pk=id) 
   
    def resolve_product_list(root, info):
        return Product.objects.all()
    def resolve_product_by_id(root, info, id):
        return Product.objects.get(pk=id)
    def resolve_product_image_list(root, info, product_id):
        print(ProductImage.objects.filter(product__id=product_id))
        return ProductImage.objects.filter(product__id=product_id)

    def resolve_application_list(root, info):
        return Application.objects.all()
    def resolve_application_by_id(root, info, id):
        return Application.objects.get(pk=id)

schema = graphene.Schema(query=Query)