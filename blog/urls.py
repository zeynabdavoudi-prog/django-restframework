from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from . import views

app_name = 'blog'
urlpatterns = [
    path('', TemplateView.as_view(template_name='blog/index.html',
                                  extra_context={'name': 'davoudi'}), name='index'),
    path(
        "go-to-django/",
        RedirectView.as_view(url="https://www.djangoproject.com/"),
        name="go-to-django",
    ),
    path('go-to-index', RedirectView.as_view(pattern_name='blog:index'), name='go-to-index'),
    path("postlist/", views.PostListView.as_view(), name="post-list"),
    path("postlist/api/", views.PostListApiView.as_view(), name="post-list-api"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post-create/", views.CreatePostView.as_view(), name="post-create"),
    path("post-update/<int:pk>/", views.UpdatePostView.as_view(), name="post-update"),
    path("post-delete/<int:pk>/", views.DeletePostView.as_view(), name="post-delete"),
    path('api/v1/', include('blog.api.v1.urls')),
    # just for test
    path('simpleview/', views.SimpleView.as_view(), name='simple_view'),
]
