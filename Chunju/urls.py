"""Chunju URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
# from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from webcore.views import account
from stark.service.v1 import site
urlpatterns = [
    re_path(r'^stark/', site.urls),
    re_path('admin/', admin.site.urls),
    path('', account.login, name='webcore_login'),
    re_path(r"rbac/", include('rbac.urls', namespace='rbac')),  # 权限管理
    re_path(r"^webapp/", include('webapp.urls', namespace='webapp')),
    # re_path(r"^", include('webcore.urls', namespace='webcore')),
    re_path(r"web/", include('web.urls', namespace='web')),
    re_path(r'webcore/', include('webcore.urls', namespace='webcore')),
    re_path(r"companysafe/", include('companysafe.urls', namespace='companysafe'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 显示上传的图片
