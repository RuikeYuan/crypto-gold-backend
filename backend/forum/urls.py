from django.urls import path

from .views import *


# Example Postman Test Scenario
# Step 1: Get the JWT Token
#
# If you're not already logged in, make sure to log in and get the JWT token. You might have an authentication API like POST /api/login/ where you pass a username and password and get back a token.
# Step 2: Create a Thread
#
# Use the POST /api/threads/ endpoint to create a new thread.
# Make sure to pass the JWT token in the Authorization header.
# Step 3: Create a Post in the Thread
#
# Use the POST /api/threads/<thread_id>/posts/ endpoint to create a new post in the thread you just created.
# Step 4: Update the Thread
#
# Use the POST /api/threads/<thread_id>/ endpoint to update the thread. Make sure the user who is trying to update the thread is the one who created it.
# Step 5: Get All Threads and Posts
#
# Use the GET /api/threads/ and GET /api/threads/<thread_id>/posts/ to list all threads and posts.

urlpatterns = [
    # List all threads and create a new thread
    path('threads/', ThreadListView.as_view(), name='thread-list'),

    # Get or update a specific thread by ID
    path('threads/<int:pk>/', ThreadDetailView.as_view(), name='thread-detail'),

    # List all posts in a specific thread and create a post in that thread
    path('threads/<int:thread_id>/posts/', CreatePostView.as_view(), name='post-list-create')
]

