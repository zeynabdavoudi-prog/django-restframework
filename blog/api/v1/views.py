from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer, CategorySerializer
from blog.models import Post, Category
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .paginations import DefaultSetPagination
# ------------------post list--------------
# function base view

# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def post_list(request):
#     if request.method == 'GET':
#         post = Post.objects.filter(status=True)
#         serializer = PostSerializer(post, many=True)
#         return Response(serializer.data)
#     else:
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class base view

# class PostListView(APIView):
#     """
#     getting a list of post and creating new post
#     """
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer
#
#     def get(self, request):
#         """
#         retrieving a list of post
#         """
#         post = Post.objects.filter(status=True)
#         serializer = self.serializer_class(post, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         """
#         creating post with provided date
#         """
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  generic view
# class PostListView(generics.ListCreateAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Post.objects.filter(status=True)


# -----------------------detail post -------------------
# function base view

# @api_view(['GET', "PUT", "DELETE"])
# def post_detail(request, id):
#
#     post = get_object_or_404(Post, id=id, status=True)
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = PostSerializer(post,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         post.delete()
#         return Response({'detail': 'item removed successfully'}, status=status.HTTP_204_NO_CONTENT)
#

# class base view

# class PostDetailView(APIView):
#     """
#     getting detail of the post and edit plus removing it
#     """
#     serializer_class = PostSerializer
#
#     def get(self, request, id):
#         """
#         retrieving the post data
#         :param request:
#         :param id:
#         :return:
#         """
#         post = get_object_or_404(Post, id=id, status=True)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
#
#     def put(self, request, id):
#         """
#         editing the post data
#         :param request:
#         :param id:
#         :return:
#         """
#         post = get_object_or_404(Post, id=id, status=True)
#         serializer = self.serializer_class(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id):
#         post = get_object_or_404(Post, id=id, status=True)
#         post.delete()
#         return Response({'detail': 'item removed successfully'}, status=status.HTTP_204_NO_CONTENT)

# generic view
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=True)
#     lookup_field = 'id'

# ------------------- view set ---------------------
# class PostViewSet(viewsets.ViewSet):
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Post.objects.filter(status=True)
#
#     def list(self, request):
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset, id=pk)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
#
#     def update(self, request, pk=None):
#         post = get_object_or_404(self.queryset, id=pk)
#         serializer = self.serializer_class(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, pk=None):
#         post = get_object_or_404(self.queryset, id=pk)
#         post.delete()
#         return Response({'detail': 'item removed successfully'}, status=status.HTTP_204_NO_CONTENT)

# ------------------ model view set ------------------
class PostModelViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'context', 'author__first_name']
    ordering_fields = ['published_date']
    pagination_class = DefaultSetPagination


class CategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()