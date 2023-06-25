from rest_framework import serializers
from .models import (
    User,
    Product,
    Order,
    Cart,
    Address,
#     UnitOfMeasure,
#     ProductImage,
#     Position,
#     ProductPrice,
#     Article,
#     Document,
    Company,
#     Category
)
# from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
# from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        if user.is_active:
            return RefreshToken.for_user(user)
        else: 
            return {'status': 'fail', 'data': 'Current account has not email confirmation'}

#     def validate(self, attrs):
#         data = super().validate(attrs)

#         refresh = self.get_token(self.user)

#         data["access"] = str(refresh.access_token)

#         return data


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True, validators=[UniqueValidator(queryset=User.objects.all())]
#     )

#     password = serializers.CharField(
#         write_only=True, required=True, validators=[validate_password]
#     )
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "password",
#             "password2",
#             "email",
#             "first_name",
#             "last_name",
#         )
#         extra_kwargs = {
#             "first_name": {"required": True},
#             "last_name": {"required": True},
#         }

#     def validate(self, attrs):
#         if attrs["password"] != attrs["password2"]:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."}
#             )

#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             email=validated_data["email"],
#             first_name=validated_data["first_name"],
#             last_name=validated_data["last_name"],
#             is_active=False
#         )

#         user.set_password(validated_data["password"])
#         user.save()

#         return user
    
# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         exclude = ("product",)

# class ProductPriceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductPrice
#         exclude = ("product",)

# class UnitOfMeasureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UnitOfMeasure
#         fields = "__all__"

# class PositionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Position
#         fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        extra_kwargs = {
            "company": {"required": False},
        }


# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = "__all__"

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = "__all__"

# class DocumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Document
#         fields = "__all__"

class CompanySerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    # def to_representation(self, instance: Company):
    #     representation = super().to_representation(instance)
    #     representation['address'] = AddressSerializer(instance.address, context=self.context, many=True).data
    #     return representation
    class Meta:
        model = Company
        fields = ('name', 'phone', 'role')
        extra_kwargs = {
            "name": {"required": False},
            "phone": {"required": False},
        }
        


class ProductSerializer(serializers.ModelSerializer):

    # def to_representation(self, instance: Product):
    #     representation = super().to_representation(instance)
    #     representation['images'] = ProductImageSerializer(instance.images.all(), many=True, context=self.context).data
    #     representation['prices'] = ProductPriceSerializer(instance.prices.all(), many=True, context=self.context).data
    #     representation['unit_of_measure'] = UnitOfMeasureSerializer(instance.unit_of_measure, context=self.context).data
    #     representation['category'] = CategorySerializer(instance.category, context=self.context).data
    #     representation['article'] = ArticleSerializer(instance.article, context=self.context).data
    #     return representation

    class Meta:
        model = Product
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    # def to_representation(self, instance: User):
    #     representation = super().to_representation(instance)
    #     representation['company'] = CompanySerializer(instance.company, context=self.context).data
    #     representation['position'] = PositionSerializer(instance.position, context=self.context).data
    #     return representation
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'company', 'position', )
        extra_kwargs = {
            "email": {"required": False},
        }



class CartSerializer(serializers.ModelSerializer):
    # def to_representation(self, instance: Cart):
    #     representation = super().to_representation(instance)
    #     representation['product'] = ProductSerializer(instance.product, context=self.context).data
    #     return representation
    cart_status = serializers.CharField()
    class Meta:
        model = Cart
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False},
        }

class OrderSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: Order):
        representation = super().to_representation(instance)
        representation['carts'] = CartSerializer(instance.carts, context=self.context, many=True).data
        representation['address'] = AddressSerializer(instance.address, context=self.context).data
        return representation
    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False},
            "total_price":{"required": False},
        }


# class EmailSerializer(serializers.Serializer):
#     email = serializers.EmailField()


# class ConfirmEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     code = serializers.CharField(min_length=6, max_length=6)
