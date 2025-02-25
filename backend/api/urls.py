from django.urls import path
from .views import user_views, post_views, tag_views, comment_views, like_views

urlpatterns = [
    # User views path
    path('user/<str:username>/', user_views.getUserProfile),
    path('users/', user_views.getUsers),
    path('users/register/', user_views.createUser),
    path('user/<str:username>/follow/', user_views.followUser),
    path('user/<str:username>/unfollow/', user_views.unfollowUser),
    
    # Post views path
    path('user/<str:username>/posts', post_views.getUserPosts),
    path('post/<str:post_id>/', post_views.getPost),
    path('post/<str:post_id>/likes/', post_views.getLikes),
    
    # Like views path
    path('post/<str:post_id>/like/', like_views.like),
    path('post/<str:post_id>/unlike/', like_views.unlike),
    
    # Comment views path
    path('post/<str:post_id>/comment/', comment_views.createComment),
    path('comment/<str:comment_id>/', comment_views.getComment),
    path('comment/<str:comment_id>/delete/', comment_views.deleteComment),
    
    # Tag views path
    
]