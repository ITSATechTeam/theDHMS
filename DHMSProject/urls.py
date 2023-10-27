from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# MSAL - AZURE AUTH SETUP
from ms_identity_web.django.msal_views_and_urls import MsalViews       
msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()

# path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),


urlpatterns = [
    path('aadmin/', admin.site.urls),
    path('', include("useronboard.urls")),
    path('member/', include("userarea.urls")),
    path('staff/', include("staffapp.urls")),
    path('auth/', include("staffapp.urls")),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    # 
    # Google auth credentials
    path('accounts/', include('allauth.urls')),
    #
    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
