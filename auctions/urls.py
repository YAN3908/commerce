from django.urls import path

from . import views

urlpatterns = [
    path("<int:lot_id>", views.lot, name="lot"),
    path("", views.index, name="index"),
    path("category/<str:category>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register/<int:lot_id>", views.register, name="registerlot"),
    path("create_lot", views.create_lot, name='create_lot')
]

