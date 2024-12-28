from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Thread, Post

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ThreadSerializer, PostSerializer

# Thread List View


def index(request):
    return HttpResponse("Hi, this is the forum")
class ThreadListView(APIView):
    """
    View to list all threads or create a new thread.
    """
    def get(self, request):
        """
        Custom GET function to list all threads.
        """
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Custom POST function to create a new thread.
        """
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new thread
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Thread Detail View
class ThreadDetailView(APIView):
    """
    View to retrieve, update or delete a specific thread.
    """
    def get(self, request, pk):
        """
        Custom GET function to fetch a specific thread by pk.
        """
        try:
            thread = Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    def post(self, request, pk):
        """
        Custom POST function to update a specific thread by pk.
        """
        try:
            thread = Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThreadSerializer(thread, data=request.data, partial=True)  # Allows partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Post View
class CreatePostView(APIView):
    """
    View to list all posts for a specific thread or create a new post.
    """
    def get(self, request, thread_id):
        """
        Custom GET function to list all posts for a specific thread.
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
        Custom POST function to create a new post in a specific thread.
        """
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {'content': request.data.get('content'), 'thread': thread.id}
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the new post
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#########################
def index(request):
    return HttpResponse("Hi, this is the forum")
class ThreadListView(ListView):
    model = Thread
    template_name = 'thread_list.html'

class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'thread_detail.html'

class CreateThreadView(CreateView):
    model = Thread
    fields = ['title']
    success_url = reverse_lazy('thread_list')
    template_name = 'create_thread.html'

class CreatePostView(CreateView):
    model = Post
    fields = ['content']
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.thread_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('thread_detail', kwargs={'pk': self.kwargs['pk']})
