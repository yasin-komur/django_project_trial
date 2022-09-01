from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from blog.dummy_data import posts
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateBlogPostForm
from django.core.paginator import Paginator


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        posts = Post.objects.filter(author__username=username).order_by("-date_posted")

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {"posts": page_obj, "is_paginated": True}
        return render(request, "blog/user_posts.html", context)


# class PostListView(View):
#
#     def get(self, request):
#         context = {"posts": Post.objects.all()}
#         return render(request, 'blog/home.html', context)


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post_detail = get_object_or_404(Post, post_id)
        context = {"object": post_detail} 
        return render(request, "blog/post_detail.html", context)


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'content']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

class PostCreateView(View):
    def get(self, request):
        form = CreateBlogPostForm()
        return render(request,'blog/post_create.html' ,{'form':form})

    def post(self, request):
        form=CreateBlogPostForm(request.POST)
        if form.is_valid():
            new_post = Post(**form.cleaned_data, author=request.user)
            new_post.save()
        return redirect('blog-home')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
#     model = Post
#     success_url = '/'
#
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

class PostDeleteView(View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('blog-home')



class HomeView(View):
    context = {
        'posts': Post.objects.all(),
    }
    template_name = 'blog/home.html'

    def get(self, request):
        return render(request, self.template_name, self.context)


class AboutView(View):
    context = {
        'posts': posts,
        'title': 'About',
    }
    template_name = 'blog/about.html'

    def get(self, request):
        return render(request, self.template_name, self.context)



