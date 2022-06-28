from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView

from dj_rest_auth.social_serializers import TwitterLoginSerializer,TwitterConnectSerializer
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from allauth.socialaccount.providers.oauth2.client import OAuth2Client



class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter

class TwitterConnect(SocialConnectView):
    serializer_class = TwitterConnectSerializer
    adapter_class = TwitterOAuthAdapter


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "CALLBACK_URL_YOU_SET_ON_GITHUB"      #####
    client_class = OAuth2Client

class GithubConnect(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "CALLBACK_URL_YOU_SET_ON_GITHUB"      #####
    client_class = OAuth2Client
    

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "CALLBACK_URL_YOU_SET_ON_GOOGLE"      #####
    client_class = OAuth2Client