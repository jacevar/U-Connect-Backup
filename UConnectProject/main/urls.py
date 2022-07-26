from re import template
from django.urls import URLPattern, path
from main.views import showmap,showroute,showRoutes,createRoute,about,register,profile,unsafe,chat
from django.conf.urls.static import static 
from django.conf import settings
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('myRoutes/',views.myRoutes,name='myRoutes'),
    path('myRoutes/<int:id>',views.myRoute,name='myRoute'),
    path('myRoutes/info/<int:id>',views.infoRoute,name='infoRoute'),
    path('myRoutes/delete/<int:id>',views.deleteRoute,name='deleteRoute'),
    path('myRoutes/update/<int:id>',views.updateRoute,name='updateRoute'),
    path('myRoutes/participants/<int:id>',views.participants,name='participants'),
    path('myRoutes/reviews/<int:id>',views.reviews,name='reviews'),
    path('joinRoute/<int:id>',views.joinRoute,name='joinRoute'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/',register, name='register'),
    path('profile/',profile, name='profile'),
    path('unsafe/',unsafe, name='unsafe'),
    path('about/',about, name='about'),
    path('setroute/<str:lat1>,<str:long1>,<str:lat2>,<str:long2>',showroute,name='showroute'),
    path('setroute/',showmap,name='showmap'),
    path('showroutes',showRoutes,name='showroutes'),
    path('createRoute',createRoute,name='createRoute'),
    path('myRoutes/chat/<int:id>/<str:username>',chat,name='chat')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)