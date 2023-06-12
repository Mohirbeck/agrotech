from .models import (
    Application,
#     Order,
    User,
#     Product,
#     ProductImage,
#     ProductPrice,
#     UnitOfMeasure,
#     Position,
#     Address,
#     Article,
#     Document,
    Company,
#     Cart,
#     Category
)
from .serializers import (
#     OrderSerializer,
#     RegisterSerializer,
    MyTokenObtainSerializer,
#     UserSerializer,
#     ProductSerializer,
#     ProductImageSerializer,
#     ProductPriceSerializer,
#     UnitOfMeasureSerializer,
#     PositionSerializer,
#     AddressSerializer,
#     ArticleSerializer,
#     DocumentSerializer,
#     CompanySerializer,
#     CartSerializer,
#     CategorySerializer,
#     EmailSerializer,
#     ConfirmEmailSerializer
)
# from .filters import (
#     CartFilter,
#     ProductFilter,
#     OrderFilter,
# )
# from .utils import send_email_code, validate_email_code
# from rest_framework.response import Response
# from rest_framework import generics, views
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, redirect
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.views import APIView
import secrets
import string
from .utils import send_email

def approve(request, id):
    application = Application.objects.get(id=id)
    company = Company.objects.create(
        name=application.name_company, phone=application.contact, role=application.type_company
    )
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20)) 
    User.objects.create_user(email=application.owner_email, password=password, company=company)
    text = f'Your password is: {password}'
    res = send_email(application.owner_email, text)
    print(res)
    if res:
        application.status = 2
        application.save()
    return redirect('/admin/agrotech/application/')


# class SendEmailView(views.APIView):
#     @swagger_auto_schema(
#         request_body=EmailSerializer(),
#     )
#     def post(self, request):
#         serializer = EmailSerializer(data=request.data)
#         if serializer.is_valid():
#             send_email_code(request, serializer.data['email'])
#             return Response(data='Code sent! check your email')
#         return Response(data=serializer.errors)


# class ConfirmEmailView(views.APIView):
#     @swagger_auto_schema(
#         request_body=ConfirmEmailSerializer(),
#     )
#     def post(self, request):
#         serializer = ConfirmEmailSerializer(data=request.data)
#         if serializer.is_valid():
#             if validate_email_code(serializer.data['email'], serializer.data['code']):
#                 return Response(data="Account is active!")
#             else:
#                 return Response(data='Code is wrong')
#         return Response(data=serializer.errors)



class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainSerializer


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer

# class ProductList(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filterset_class = ProductFilter

# class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class CartView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     filterset_class = CartFilter

# class CartDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

# class CategoryList(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# class CategoryDetail(generics.RetrieveAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# class OrderView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     filterset_class = OrderFilter

# class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
