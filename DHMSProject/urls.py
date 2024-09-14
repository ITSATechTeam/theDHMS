from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi



# MSAL - AZURE AUTH SETUP
from ms_identity_web.django.msal_views_and_urls import MsalViews       
msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()

# path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),

schema_view = get_schema_view(
    openapi.Info(
        title="The DHMS API",
        default_version='v2',
        description="DHMS API Documentation",
        terms_of_service="https://itservicedeskafrica.com/wp-content/uploads/2023/07/ITSA-POLICIES-1.pdf",
        contact=openapi.Contact(email="franklin.i@itservicedeskafrica.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("useronboard.urls")),
    path('member/', include("userarea.urls")),
    path('staff/', include("staffapp.urls")),
    path('auth/', include("staffapp.urls")),
    path('familydhms/', include("familydhmsapp.urls")),
    path('superadmin/', include("dhmsadminboard.urls")),
    path('api/', include("dhmsapiapp.urls")),
    path('aichat/', include("aichat.urls")),
    path('student/', include("studentdhms.urls")),
    path('comm/', include("commapp.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    # 
    # Google auth credentials
    # path('', include('googleauthentication.urls')),
    path('accounts/', include('allauth.urls')),
    #
    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
    # PWA
    path('', include("pwa.urls")),
]


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


