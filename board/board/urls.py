"""board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from base import views
from user import views as user_views
from rent import views as rent_views
from reviews import views as reviews_views
from base import views as base_views
from payment import views as stripe_views


from rent.views import new_game
from rent import forms as rent_forms
from rent.forms import NewGame

urlpatterns = [
    #Main
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login', user_views.login),
    path('logout', user_views.logout),
    path('base/', views.base),
    path('terms/', views.terms),
    path('privacy/', views.privacy),

    #Rent
    path('games/', rent_views.games_list),
    path('gamesFav/', rent_views.juegosFav),
    re_path(r'gamesFavAdd/(?P<id_game>\d+)', rent_views.add_juegos_fav),
    re_path(r'gamesFavDelete/(?P<id_game>\d+)', rent_views.delete_juegos_fav),
    path('delete/<int:pk>', rent_views.delete),
    path('myGames/', rent_views.games_list_by_user),
    path('gameDetail/<int:pk>/', rent_views.games_detail, name='games_detail'),
    path('newgame', rent_views.new_game),
    path('gameDetail/<int:pk>/edit/', rent_views.edit_game, name='new_game'),
    path('gameDetail/<int:pk>/pic/', rent_views.edit_pic, name='new_game'),
    re_path(r'rent/(?P<id_game>\d+)',rent_views.rent_game),
    re_path(r'rents/(?P<id_user>\d+)',rent_views.rents_list),
    re_path(r'cart/',rent_views.view_cart),
    re_path(r'addCart/(?P<id_game>\d+)', rent_views.add_item_to_cart),
    re_path(r'deleteCart/(?P<id_item>\d+)', rent_views.delete_item_from_cart),
    re_path(r'deleteAll/', rent_views.empty_cart),
    re_path(r'games/filterZona/(?P<zona>\d+)', rent_views.games_list_by_zona),
    re_path(r'games/filterStatus/(?P<status>\d+)', rent_views.games_list_by_status),
    path('rents/deliver/<int:pk>/', rent_views.deliver),
    path('gameDetail/<int:pk>/rents/', rent_views.game_rents),
    re_path(r'games/filterDistance/', rent_views.games_list_by_distance),

    #User
    re_path(r'profile/(?P<id_user>\d+)',user_views.profile),
    path('newuser', user_views.new_user),
    path('deleteUser/<int:pk>', user_views.delete_myUSer),
    path('editPassword/', user_views.edit_pass),
    path('editUsername/', user_views.edit_username),
    path('editProfile/', user_views.edit_profile),
    path('editPic/', user_views.edit_pic),
    path('users/', user_views.user_list),
    path('contact/<int:pk>', user_views.contact_user),
    path('obtenerDatos/<int:pk>', user_views.DescargaDatosUser),
    path('premium/', user_views.premium),

    #Review
    re_path(r'review/(?P<id_user>\d+)',reviews_views.create_review),
    re_path(r'comments/(?P<id_user>\d+)',reviews_views.list_comments),

    #Stripe
    re_path(r'charge/(?P<id_cart>\d+)', stripe_views.charge),
    re_path(r'confirm/(?P<id_cart>\d+)/', stripe_views.confirm),
    path('success/', stripe_views.pago_completado),
    path('contend/<int:pk>', stripe_views.new_contend),
    path('contends/', stripe_views.contend_list),
    path('contend/<int:pk>/detail', stripe_views.contend_detail),
    path('compensation/<int:pk>/new/', stripe_views.new_compensation),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)