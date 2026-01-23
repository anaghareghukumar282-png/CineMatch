from django.urls import path 
from . import views
urlpatterns=[
    path('userhome/',views.userhome,name='userhome'),
    path('profile/',views.profile,name='profile'),
    path('preferences/',views.preferences,name='preferences'),
    path('save-preferences/',views.save_preferences,name='save_preferences'),
    path('browse-movies/',views.browse_movies,name='browse_movies'),
    path('add-to-watchlist/<int:movie_id>/',views.add_to_watchlist,name='add_to_watchlist'),
    path('watchlist/',views.view_watchlist,name='view_watchlist'),
    path('remove-from-watchlist/<int:watch_id>/',views.remove_from_watchlist,name='remove_from_watchlist'),
]