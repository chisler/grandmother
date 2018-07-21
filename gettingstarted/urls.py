from django.conf.urls import url
from django.urls import path

from django.contrib import admin

from profiles.api.views import UserProfileGet
from users.api.views import UserCreate
from rest_framework.authtoken import views as restframework_views
admin.autodiscover()

urlpatterns = [
    url(r'users/create/', UserCreate.as_view(), name='user-create'),
    url(r'^profile/', UserProfileGet.as_view(), name='profile-get'),
    url(r'^api-token-auth/', restframework_views.obtain_auth_token),
    path('admin/', admin.site.urls),

]
