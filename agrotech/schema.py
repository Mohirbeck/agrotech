import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from .serializers import CompanySerializer, UserSerializer, CartSerializer, ProductSerializer, AddressSerializer,OrderSerializer

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
    CartProduct,
    Category,
    Application
)
import graphql_jwt


class OrderCreateMutation(SerializerMutation):
    class Meta:
        serializer_class = OrderSerializer
        model_operations = ['create']

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        instance = Order(user=info.context.user)
        user_active_carts = Cart.objects.filter(user=info.context.user, cart_status=Cart.Status.ACTIVE)
        for active_cart in user_active_carts:
            product_cart = CartProduct.objects.create( )
        # input['user'] = info.context.user
        if instance:
            return {'instance': instance, 'data': input, 'partial': True}

        else:
            raise 'http.Http404'
        print(input, cls, info)
        return {'data': input, 'partial': True}

    

class DeleteCartMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    status = graphene.String()
    @classmethod
    def mutate(cls, root, info,  id):
        cart = Cart.objects.get(pk=id)
        cart.delete()
        return DeleteCartMutation(status='success')
    

class UpdateCartMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        quantity = graphene.ID()
    status = graphene.String()
    @classmethod
    def mutate(cls, root, info,  id, quantity):
        cart = Cart.objects.get(pk=id)
        cart.quantity = quantity
        cart.save()
        return DeleteCartMutation(status='success')


class CartModelMutation(SerializerMutation):
    class Meta:
        serializer_class = CartSerializer
        model_operations = ['create']
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        instance = Cart(user=info.context.user)
        # input['user'] = info.context.user
        if instance:
            return {'instance': instance, 'data': input, 'partial': True}

        else:
            raise 'http.Http404'
        print(input, cls, info)
        return {'data': input, 'partial': True}
       

class AdressModelCreateMutation(SerializerMutation):
    class Meta:
        serializer_class = AddressSerializer
        model_operations = ['create']
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        instance = Address(company=info.context.user.company)
        # input['user'] = info.context.user
        if instance:
            return {'instance': instance, 'data': input, 'partial': True}

        else:
            raise 'http.Http404'
        print(input, cls, info)
        return {'data': input, 'partial': True}
    

class AdressModelUpdateMutation(SerializerMutation):
    class Meta:
        serializer_class = AddressSerializer
        model_operations = ['update']
        lookup_field = 'id'

class AdressModelDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    status = graphene.String()
    @classmethod
    def mutate(cls, root, info,  id):
        cart = Address.objects.get(pk=id)
        cart.delete()
        return DeleteCartMutation(status='success')
    
    # @classmethod
    # def get_serializer_kwargs(cls, root, info, **input):
    #     instance = Address(company=info.context.user.company)
    #     # input['user'] = info.context.user
    #     if instance:
    #         return {'instance': instance, 'data': input, 'partial': True}

    #     else:
    #         raise 'http.Http404'
    #     print(input, cls, info)
    #     return {'data': input, 'partial': True}


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
        print(input['role'][0])
        instance = Company.objects.get(
            id=info.context.user.company.id
        )
        if instance:
            return {'instance': instance, 'data': input, 'partial': True}

        else:
            raise 'http.Http404'

        return {'data': input, 'partial': True}


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    update_company = CompantModelMutation.Field()
    update_user = UserModelMutation.Field()

    create_cart = CartModelMutation.Field()
    delete_cart = DeleteCartMutation.Field()
    update_cart = UpdateCartMutation.Field()

    create_address = AdressModelCreateMutation.Field()
    update_address = AdressModelUpdateMutation.Field()
    delete_address = AdressModelDeleteMutation.Field()

    create_order = OrderCreateMutation.Field()


class OrderType(DjangoObjectType):

    class Meta:
        model = Order
        fields = '__all__'


class CartProductType(DjangoObjectType):

    class Meta:
        model = CartProduct
        fields = '__all__'

class AddressType(DjangoObjectType):

    class Meta:
        model = Address
        fields = '__all__'

class CartType(DjangoObjectType):
    cart_status = graphene.String()
    class Meta:
        model = Cart
        fields = '__all__'


class ProductImageType(DjangoObjectType):

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'created_at', 'updated_at')

class CompanyType(DjangoObjectType):
    role = graphene.Int()
    class Meta:
        model = Company
        fields = '__all__'

class UnitOfMeasureType(DjangoObjectType):

    class Meta:
        model = UnitOfMeasure
        fields = '__all__'

class ArticleType(DjangoObjectType):

    class Meta:
        model = Article
        fields = '__all__'

class CategoryType(DjangoObjectType):

    class Meta:
        model = Category
        fields = '__all__'


class ProductType(DjangoObjectType):

    class Meta:
        model = Product
        fields = '__all__'


class ApplicationType(DjangoObjectType):

    class Meta:
        model = Application
        fields = '__all__'


class Query(graphene.ObjectType):

    application_list = graphene.List(ApplicationType)
    application_by_id = graphene.Field(ApplicationType, id=graphene.String())

    product_list = graphene.List(ProductType)
    product_by_id = graphene.Field(ProductType, id=graphene.String())
    product_image_list = graphene.List(ProductImageType, product_id=graphene.String())
    
    category_list = graphene.List(CategoryType)
    category_by_id = graphene.Field(CategoryType, id=graphene.String())

    company_list = graphene.List(CompanyType)

    my_carts = graphene.List(CartType)

    address_list = graphene.List(AddressType) 

    my_orders = graphene.List(OrderType)

    cart_product_list = graphene.List(CartProductType, order_id=graphene.String())

    def resolve_my_orders(root, info):
        if not info.context.user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user=info.context.user) 
    
    def resolve_cart_product_list(root, info, order_id):
        if not info.context.user.is_authenticated:
            return CartProduct.objects.none()
        return CartProduct.objects.filter(ordeer__id=order_id) 

    def resolve_address_list(root, info):
        if not info.context.user.is_authenticated:
            return Address.objects.none()
        return Address.objects.filter(company=info.context.user.company) 
        
    def resolve_my_carts(root, info):
        if not info.context.user.is_authenticated:
            return Cart.objects.none()
        return Cart.objects.filter(user=info.context.user) 
    def resolve_company_list(root, info):
        return Company.objects.all()
    def resolve_category_list(root, info):
        if info.context.user.is_authenticated:
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