from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Mailing API',
        default_version='v0.1',
        description='Test assignment for Fabrique. Mailing API',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='test@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r'^docs(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(
        r'^docs/$',
        schema_view.with_ui('swagger',cache_timeout=0),
        name='schema-swagger-ui',
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
    path('api/', include('mailings.urls')),
]
