from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path("<int:lot_id>", views.lot, name="lot"),
                  path("mylots", views.mylots, name="mylots"),
                  path("mybids", views.mybids, name="mybids"),
                  path("", views.index, name="index"),
                  path("category/<str:category>", views.category, name="category"),
                  path("login", views.login_view, name="login"),
                  path("logout", views.logout_view, name="logout"),
                  path("register", views.register, name="register"),
                  path("register/<int:lot_id>", views.register, name="registerlot"),
                  path("create_lot", views.create_lot, name='create_lot')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
