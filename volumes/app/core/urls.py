"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from dj_rest_auth.registration.views import VerifyEmailView
# from dj_rest_auth.views import PasswordResetConfirmView

from emails.views import VerifyEmailView, CheckEmailAddressView
from emails.views import EmailPasswordResetView, EmailPasswordResetConfirmView



# from core.views import (FacebookLogin,
#                         TwitterLogin,
#                         GithubLogin,
#                         GoogleLogin,
#                         FacebookConnect,
#                         TwitterConnect,
#                         GithubConnect)

# from dj_rest_auth.registration.views import (SocialAccountListView, 
#                                             SocialAccountDisconnectView)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/account-confirm-email/',  VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('auth/account-check-email/',    CheckEmailAddressView.as_view(), name='account_email_check'),
    path('auth/reset-password/reset/',   EmailPasswordResetView.as_view(), name='rest_password_by_email'),
    path('auth/reset-password/confirm/', EmailPasswordResetConfirmView.as_view(), name='confirm_rest_password_by_email'),
    # path('user/reset-password/<slug:uidb64>/<slug:token>/',
    #     PasswordResetConfirmView.as_view(), 
    #     name='password_reset_confirm'),
    
    # project routes
    path('balance/', include('balance.urls')),
    path('binance/', include('binanceWallet.urls')),
    path('contract/', include('contract.urls')),
    path('events/', include('events.urls')),
    path('secrets/', include('keysecrets.urls')),
    path('orders/', include('orders.urls')),
    path('profile/', include('profiles.urls')),
    path('trades/', include('trades.urls')),
    path('userstrategy/', include('userstrategies.urls')),
    
    path('usertotal/', include('total.urls')),
    
    # social login
    # path('auth/facebook/login/', FacebookLogin.as_view(), name='fb_login'),
    # path('auth/twitter/login/', TwitterLogin.as_view(), name='twitter_login'),
    # path('auth/github/login/', GithubLogin.as_view(), name='github_login'),
    # path('auth/google/login/', GoogleLogin.as_view(), name='google_login'),

    # social connect
    # path('auth/facebook/connect/', FacebookConnect.as_view(), name='fb_connect'),
    # path('auth/twitter/connect/', TwitterConnect.as_view(), name='twitter_connect'),
    # path('auth/github/connect/', GithubConnect.as_view(), name='github_connect'),
]

# urlpatterns += [
#     path('socialaccounts/', SocialAccountListView.as_view(),name='social_account_list'),
#     path('socialaccounts/<int:pk>/disconnect/',SocialAccountDisconnectView.as_view(),name='social_account_disconnect'),
# ]

urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
