from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from blog.dummy_data import posts
from .models import Post
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateBlogPostForm
from django.core.paginator import Paginator
from .forms import CommentForm
from django.http import HttpResponseRedirect
# annotate, agreegate, ORM, jquery-html-ajax (sayfa yenileme), javascript, view parçalama, biraz daha karmaşık yazma,
# crud yorum için de, başka crud uğraşma, ekranlara filtreler uygula, toplam okuma, üye sayısı, bir kişi 2 farklı kulüpte aynı postu yayınlayabilir,
# basketol-beşiktaş, chat eklenebilir


class PostListView(View):
    def get(self, request, *args, **kwargs):
        data = Post.objects.all().order_by("-date_posted")
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {"posts": page_obj, "is_paginated": True}
        return render(request, "blog/home.html", context)


class UserPostListView(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        posts = Post.objects.filter(
            author__username=username).order_by("-date_posted")

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {"posts": page_obj, "is_paginated": True}
        template_name = "blog/user_posts.html"
        return render(request, template_name, context)


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post_detail = get_object_or_404(Post, id=post_id)
        # form = CommentForm(request.POST)
        context = {"object": post_detail, "post": posts}
        template_name = "blog/post_detail.html"
        return render(request, template_name, context)


class PostCreateView(LoginRequiredMixin, View, UserPassesTestMixin):
    login_url = '/login/'
    redirect_field_name = 'blog-home'

    def get(self, request):
        form = CreateBlogPostForm()
        return render(request, 'blog/post_form.html', {'form': form})

    def post(self, request):
        form = CreateBlogPostForm(request.POST)
        if form.is_valid():
            new_post = Post(**form.cleaned_data, author=request.user)
            new_post.save()
        return redirect('blog-home')


class PostUpdateView(LoginRequiredMixin, View, UserPassesTestMixin):
    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        obj = Post.objects.get(id=post_id)
        form = CreateBlogPostForm(instance=obj)
        return render(request, "blog/post_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        obj = Post.objects.get(id=post_id)
        form = CreateBlogPostForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('blog-home')


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


class LikeView(View):

    def get(self, request, pk):
        post = get_object_or_404(Post, request.POST.get('post_id'))
        post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

