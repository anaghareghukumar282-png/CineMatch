from django.urls import path 
from . import views
from userapp.views import account, view_community
urlpatterns=[
    path('userhome/',views.userhome,name='userhome'),
    path('profile/',views.profile,name='profile'),
    path('account/',views.account,name='account'),
    path('preferences/',views.preferences,name='preferences'),
    path('save-preferences/',views.save_preferences,name='save_preferences'),
    path('browse-movies/',views.browse_movies,name='browse_movies'),
    path('add-to-watchlist/<int:movie_id>/',views.add_to_watchlist,name='add_to_watchlist'),
    path('watchlist/',views.view_watchlist,name='view_watchlist'),
    path('remove-from-watchlist/<int:watch_id>/',views.remove_from_watchlist,name='remove_from_watchlist'),
    path('view-community/',views.view_community,name='view_community'),
    path('create-community/',views.create_community,name='create_community'),
    path('join-community/<int:community_id>/',views.join_community,name='join_community'),
    path('community-chat/<int:community_id>/',views.community_chat,name='community_chat'),
    path('send-community-message/<int:community_id>/',views.send_community_message,name='send_community_message'),
    path('view-discussions/',views.view_discussions,name='view_discussions'),
    path('new-discussion/',views.new_discussion,name='new_discussion'),
    path('discussion-detail/<int:discussion_id>/',views.discussion_detail,name='discussion_detail'),
    path('change-password/',views.change_password,name='change_password'),
]