from django.conf.urls import url
from django.urls import path

from django.contrib import admin

from users.api.views import UserCreate
from rest_framework.authtoken import views as restframework_views
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    # url(r'^users/', include('users.urls')),
    url(r'users/create/', UserCreate.as_view(), name='user-create'),
    url(r'^api-token-auth/', restframework_views.obtain_auth_token),
    path('admin/', admin.site.urls),

]
