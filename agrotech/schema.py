import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from .serializers import CompanySerializer, UserSerializer
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
import graphql_jwt


class UserModelMutation(SerializerMutation):
    class Meta:
        serializer_class = UserSerializer
        model_operations = ['update']

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        instance = User.objects.get(
            id=info.context.user.id
        )
        if instance:
            return {'instance': instance, 'data': input, 'partial': True}

        else:
            raise 'http.Http404'

        return {'data': input, 'partial': True}

class CompantModelMutation(SerializerMutation):
    class Meta:
        serializer_class = CompanySerializer
        model_operations = ['update']

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        # print(info.context.user.id)
        u = User.objects.get(id=info.context.user.id)
        print(u.company)
        instance = Company.objects.get(
            id=info.context.user.company.id
        )
        if instance:
            return {'instance': instance, 'data': input, 'partial': True}

        else:
            raise 'http.Http404'

        return {'data': input, 'partial': True}

class Mutation(graphene.ObjectType):
    # def process_response(self, request, response):
    #     if (self.request_has_cookie_mutation(request)):
    #         new_cookie = 'salut bratan'
    #         response.set_cookie('wanted_cookie', new_cookie)
    #     return response
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    update_company = CompantModelMutation.Field()
    update_user = UserModelMutation.Field()

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

    company_list = graphene.List(CompanyNode)

    def resolve_company_list(root, info):
        return Company.objects.all()
    def resolve_category_list(root, info):
        print('Rabotayet')
        print(root)
        print(info)
        print(info.context.user)
        if info.context.user.is_authenticated:
            print('ISHLADI PIDARAS')
            return Category.objects.none()
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

schema = graphene.Schema(query=Query, mutation=Mutation)    