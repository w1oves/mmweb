"""dl3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from login.views import index, signin, signup

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", index, name="index"),
    path("index/", index, name="index"),
    path("signup/", signup, name="signup"),
    path("signin/<str:user_name>", signin, name="signin"),
    path("signin/", signin, name="signin"),
    path("main/", include("main.urls")),
    url(r"mdeditor/", include("mdeditor.urls")),
]
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
