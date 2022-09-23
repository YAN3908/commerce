"""commerce URL Configuration

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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from auctions.views import *
from rest_framework import routers

# router=routers.SimpleRouter()
# router.register(r'lot', LotViewSet)

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("", include("auctions.urls")),
                  path("api/v1/drf-auth/", include('rest_framework.urls')),
                  # path("api/v1/", include(router.urls))  #  http://127.0.0.1:8000/api/v1/lot/
                  # path("api/v1/lotlist", LotViewSet.as_view({'get': 'list'})),
                  # path("api/v1/lotlist/<int:pk>", LotViewSet.as_view({'put': 'update'})),
                  # path("api/v1/lotapidetail/<int:pk>", LotAPIDetailVew.as_view())
                  path("api/v1/lot", LotAPIList.as_view()),
                  path("api/v1/lot/<int:pk>", LotAPIUpdate.as_view()),
                  path("api/v1/lotapidelete/<int:pk>", LotAPIDestroy.as_view())
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
