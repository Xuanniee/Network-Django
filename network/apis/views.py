# Import Viewsets (aka Views outside of REST)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from network.models import Post
from .serializers import PostEasySerializer, PostSerializer

# Trying
class PostListCreateAPIView(ListCreateAPIView):
    """
    API View to retrieve List of Posts New Posts
    """
    #permission_classes = (IsAuthenticated, )
    serializer_class = PostEasySerializer
    queryset = Post.objects.all()

class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API View to retrieve, update, or destroy post
    """
    #permission_classes = (IsAuthenticated, )
    serializer_class = PostEasySerializer
    queryset = Post.objects.all()

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True 
        return self.update(request, *args, **kwargs)



# Create Viewset
class PostViewset(viewsets.ModelViewSet):
    # Define QuerySet
    queryset = Post.objects.all()

    # Specify which Serializer we are using
    serializer_class = PostEasySerializer

class PostView(APIView):
    # GET Request
    def get(self, request):
        posts = Post.objects.all()
        # Many Argument means more than 1 Post will be Serialized
        serializer = PostSerializer(posts, many=True)
        return Response({"posts": serializer.data})

    # POST Request
    def post(self, request):
        # Retrieve Contents of Post from User
        post = request.data.get('post')

        # Create a Post from the Data provided
        serializer = PostSerializer(data=post)
        if serializer.is_valid(raise_exception=True):
            post_saved = serializer.save()

        # Return Response
        return Response({"success": "Post {} created successfully!!".format(post_saved.post_content)})