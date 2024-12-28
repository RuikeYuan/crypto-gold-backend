from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='forum_index'),
    path('threads/', ThreadListView.as_view(), name='thread_list'),
    #path('threads/<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),  # GET (thread details) + POST (update thread)
   # path('threads/<int:thread_id>/posts/', CreatePostView.as_view(), name='create_post'),  # GET (list posts) + POST (create post)
   # path('create/', CreateThreadView.as_view(), name='create_thread'),
    path('reply/', CreatePostView.as_view(), name='create_post'),
    path('thread/<slug:slug>/', ThreadDetailView.as_view(), name='thread_detail'),
]