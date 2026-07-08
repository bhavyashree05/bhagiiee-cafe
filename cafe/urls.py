from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/",views.menu, name="menu"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("order/<int:item_id>/", views.place_order, name="place_order"),
    path("payment/<int:order_id>/", views.payment, name="payment"),
    path("receipt/<int:order_id>/", views.receipt, name="receipt"),
    path("history/", views.order_history, name="order_history"),
    path("dashboard/", views.admin_dashboard, name="dashboard"),
]
