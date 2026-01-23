from django.urls import path 
from .import views
urlpatterns=[
#this is used to call the message function in views.py nammal simpleappil create cheythathu athil thanne olla url pattern aanu ithu appo ithil tanne olla urls.py il thanne views.py il create cheytha message function ne call cheyyunnu
path('', views.adminindex, name='adminindex'),
path('adminindex/', views.adminindex, name='adminindex'),
path('view_users/', views.view_users, name='view_users'),
path('user_detail/<int:userid>/', views.user_detail, name='user_detail'),
path('reports/', views.generate_reports, name='generate_reports'),
path('genre/',views.genres,name='genre'),
path('genre_insert/',views.genre_insert,name='genre_insert'),
path('viewgenre/',views.viewgenre,name='viewgenre'),
path('editgenre/<genreid>/',views.editgenre,name='editgenre'),
path('deletegenre/<genreid>/',views.deletegenre,name='deletegenre'),
path('language/',views.languages,name='language'),
path('language_insert/',views.language_insert,name='language_insert'),
path('viewlanguage/',views.viewlanguage,name='viewlanguage'),
path('editlanguage/<languageid>/',views.editlanguage,name='editlanguage'),  
path('deletelanguage/<languageid>/',views.deletelanguage,name='deletelanguage'),
path('movie/',views.movie,name='movie'),
path('movie_insert/',views.movie_insert,name='movie_insert'),
path('viewmovie/',views.viewmovie,name='viewmovie'),
path('editmovie/<movieid>/',views.editmovie,name='editmovie'),
path('deletemovie/<movieid>/',views.deletemovie,name='deletemovie'),
]