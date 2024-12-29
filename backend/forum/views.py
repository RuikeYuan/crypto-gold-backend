from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Thread, Post
from .serializers import ThreadSerializer, PostSerializer


class ThreadListView(APIView):
    """
    View to list all threads or create a new thread.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all threads.
        """
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new thread. The user must be authenticated.
        """
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_403_FORBIDDEN)

        # Add the user to the request data
        request.data['user'] = request.user.id
        serializer = ThreadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Save the new thread with the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadDetailView(APIView):
    """
    View to retrieve, update or delete a specific thread.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Fetch a specific thread by pk.
        """
        try:
            thread = Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    def post(self, request, pk):
        """
        Update a specific thread. User must be the one who created the thread.
        """
        try:
            thread = Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the owner of the thread
        if thread.user != request.user:
            return Response({'error': 'You do not have permission to edit this thread.'},
                            status=status.HTTP_403_FORBIDDEN)

        data = {
            'content': request.data.get('content', thread.content),
            'title': request.data.get('title', thread.title)
        }

        serializer = ThreadSerializer(thread, data=data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePostView(APIView):
    """
    View to list all posts for a specific thread or create a new post.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, thread_id):
        """
        List all posts in a specific thread.
        """
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(thread=thread)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, thread_id):
        """
        Create a new post in a specific thread. The user must be authenticated.
        """
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_403_FORBIDDEN)

        data = {'content': request.data.get('content'), 'thread': thread.id, 'user': request.user.id}
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()  # Save the new post with the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """
    View to update a specific post. The user must be the one who created the post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Update a specific post. User must be the one who created the post.
        """
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the owner of the post
        if post.user != request.user:
            return Response({'error': 'You do not have permission to edit this post.'},
                            status=status.HTTP_403_FORBIDDEN)

        data = {
            'content': request.data.get('content', post.content),
        }

        serializer = PostSerializer(post, data=data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
