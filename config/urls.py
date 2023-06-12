from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from agrotech.views import  MyObtainTokenPairView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

schema_view = get_schema_view(
   openapi.Info(
      title="AGROTECH BACKEND",
      default_version='v1',
      description="",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
   #  path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', include('agrotech.urls'))
]
