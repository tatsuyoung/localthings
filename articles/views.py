import json
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from accounts.models import Profile
from .models import Article, Comment
from. import forms


def article_list(request):
    articles_list = Article.objects.all().order_by('-date')
    paginator = Paginator(articles_list, 24)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    query = request.GET.get("q")
    if query:
        articles = articles_list.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
            ).distinct()
    return render(request, 'articles/article_list.html', {'articles': articles})


def article_detail(request, detail_id):
    article = Article.objects.get(id=detail_id)
    return render(request, 'articles/article_detail.html', {'article': article})


@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form': form})


@require_POST
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return redirect('articles:list')


@login_required(login_url="/accounts/login/")
@require_POST
def article_comment(request, pk):
    article_com = Article.objects.get(id=pk)
    comments = Comment.objects.filter(post=article_com)
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = article_com
            comment.author = request.user
            comment.save()
    else:
        form = forms.CommentForm()

    context = {'article': article_com,
               'form': form,
               'comments': comments
               }
    return render(request, 'articles/article_detail.html', context)


@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('articles:list')


@require_POST
def like_button(request, like_id):

    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        article = get_object_or_404(Article, slug=slug, id=like_id)

        if article.like.filter(id=user.id).exists():
            article.like.remove(user)
            message = 'You disliked this'
        else:
            article.like.add(user)
            message = 'You liked this'

    context = dict(likes_count=article.total_likes, message=message)
    return HttpResponse(json.dumps(context), content_type='application/json')


def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    my_article = user.article_set.all().order_by('-date')
    paginator = Paginator(my_article, 24)
    page = request.GET.get('page')
    my_article = paginator.get_page(page)

    context = {
                'user': user,
                'my_article': my_article
                }
    return render(request, 'articles/users_detail.html', context)


def users_detail_comments(request, pk):
    article_com = Article.objects.get(id=pk)
    comments = Comment.objects.filter(post=article_com)

    context = {
                'article': article_com,
                'comments': comments
               }
    return render(request, 'articles/users_detail_comments.html', context)


def users_detail_liked(request, pk):
    article_title = Article.objects.get(id=pk)
    articles = Article.objects.filter(title=article_title)
    context = {
                'articles': articles
                }
    return render(request, 'articles/users_detail_like.html', context)


@login_required(login_url="/accounts/login/")
def article_edit(request, pk):
    if id:
        post = get_object_or_404(Article, pk=pk)
        if post.author != request.user:
            return HttpResponseForbidden()
    else:
        post = Article(author=request.user)

    form = forms.CreateArticle(request.POST, request.FILES, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle(instance=post)
    context = {'form': form}
    return render(request, 'articles/article_edit.html', context)


class UserPostListView(ListView):
    model = Article
    template_name = 'articles/user_post_list.html'
    context_object_name = 'articles'
    paginate_by = 9

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context


class AuthorProfileView(ListView):
    model = Profile
    template_name = 'articles/author_profile_view.html'
    context_object_name = 'profiles'
    allow_empty = False

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])


class Gallery(ListView):
    model = Article
    template_name = 'articles/article_photo_gallery.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.all().order_by('-date')


class ArticleOrderedByLikes(ListView):
    model = Article
    template_name = 'articles/article_ordered_by_likes.html'
    context_object_name = 'articles'
    paginate_by = 9

    def get_queryset(self):
        return Article.objects.annotate(like_count=Count('like')).order_by('-like_count')