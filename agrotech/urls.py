from django.urls import path

from . import views

urlpatterns = [
    path('approve/<int:id>/', views.approve, name="approve")
#     path("register/", views.RegisterView.as_view(), name="register"),
#     path("login/", views.MyObtainTokenPairView.as_view(), name="login"),
#     path("product/", views.ProductList.as_view(), name="product"),
#     path("product/<int:pk>/", views.ProductDetail.as_view(), name="product_detail"),
#     path("cart/", views.CartView.as_view(), name="cart"),
#     path("cart/<int:pk>/", views.CartDetail.as_view(), name="cart_detail"),
#     path("category/", views.CategoryList.as_view(), name="category"),
#     path("category/<int:pk>/", views.CategoryDetail.as_view(), name="category_detail"),
#     path("order/", views.OrderView.as_view(), name="order"),
#     path("order/<int:pk>/", views.OrderDetail.as_view(), name="order_detail"),
#     # path("email/send/", views.SendEmailView.as_view()),
#     # path("email/confirm/", views.ConfirmEmailView.as_view()),
    
]