from django.urls import path
from . import views

app_name = 'api-v1'
urlpatterns = [
    # path('post-list/', views.post_list, name='post-list'),
    # path('post-list/', views.PostListView.as_view(), name='post-list'),
    # path('post-detail/<int:id>/', views.post_detail, name='post-detail'),
    # path('post-detail/<int:id>/', views.PostDetailView.as_view(), name='post-detail'),
    # path('post-list/', views.PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    # path('post-detail/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
    #      , name='post-detail'),
    path('post-list/', views.PostModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    path('post-detail/<int:pk>/', views.PostModelViewSet.as_view
    ({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         , name='post-detail'),
    path('category-list/', views.CategoryModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('category-detail/<int:pk>/', views.CategoryModelViewSet.as_view
    ({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         , name='category-detail'),


]
