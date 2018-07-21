from django.conf.urls import url
from django.urls import path

from django.contrib import admin

from users.api.views import UserCreate, UserProfileGet, GetTraders
from rest_framework.authtoken import views as restframework_views
admin.autodiscover()

urlpatterns = [
    url(r'users/create/', UserCreate.as_view(), name='user-create'),
    url(r'^user/(?P<user_id>\d+)/$', UserProfileGet.as_view(), name='profile-get'),
    url(r'^traders/$', GetTraders.as_view(), name='traders'),
    url(r'^api-token-auth/', restframework_views.obtain_auth_token),
    path('admin/', admin.site.urls),

]
