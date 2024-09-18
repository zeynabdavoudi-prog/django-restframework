from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from .models import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(60 * 15), name='dispatch')
class PostListView(PermissionRequiredMixin, ListView):
    permission_required = ['blog.view_post']
    queryset = Post.objects.filter(status=True)
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post_list.html'

@method_decorator(cache_page(60 * 15), name='dispatch')
class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = 'blog/post_detail.html'


class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'context', 'image', 'category']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        author = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)

    success_url = '/blog/postlist/'


class UpdatePostView(UpdateView):
    model = Post
    fields = ['title', 'context', 'image', 'category']
    template_name = 'blog/post_form.html'
    success_url = '/blog/postlist/'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/blog/postlist/'


# just for test
class SimpleView(View):
    def get(self, request):
        return render(request, 'blog/simple.html')


class PostListApiView(TemplateView):
    template_name = 'blog/postlist_api.html'