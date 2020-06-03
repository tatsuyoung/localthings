import json
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from accounts.models import Profile
from .models import Article, Comment, Category
from. import forms


def article_list(request):
    users = Profile.objects.all().order_by('?')[:4]
    articles_list = Article.objects.all().order_by('-date')
    order_like_articles = articles_list.annotate(like_count=Count('like')).order_by('?')[:5]
    paginator = Paginator(articles_list, 24)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    query = request.GET.get("q")
    if query:
        articles = articles_list.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
            ).distinct()
    return render(request, 'articles/article_list_new.html',
                  {'articles': articles,
                   'order_like_articles': order_like_articles,
                   'users': users
                   }
                  )


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
    comments = Comment.objects.filter(post=article_com).order_by('created_date')
    current_user = request.user
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = article_com
            comment.author = request.user
            comment.save()
    else:
        form = forms.CommentForm()
    context = {
                'article': article_com,
                'form': form,
                'comments': comments,
                'current_user': current_user
               }
    return render(request, 'articles/article_detail.html', context)


@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('articles:list')


@login_required(login_url="/accounts/login/")
def book_mark_list(request):
    user = request.user
    my_book_mark = user.book_mark.all().order_by('-date')
    context = {
        'my_book_mark': my_book_mark
    }
    return render(request, 'articles/article_book_mark.html', context)


@require_POST
def book_mark(request, book_mark_id):

    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title', None)
        article = get_object_or_404(Article, title=title, id=book_mark_id)

        if article.book_mark.filter(id=user.id).exists():
            article.book_mark.remove(user)
            message = 'Book Markから外しました。'
        else:
            article.book_mark.add(user)
            message = 'Book Markしました。'
    context = dict(message=message)
    return HttpResponse(json.dumps(context), content_type='application/json')


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
    current_user = request.user
    user = get_object_or_404(User, pk=current_user.pk)
    my_article = user.article_set.all().order_by('-date')
    paginator = Paginator(my_article, 9)
    page = request.GET.get('page')
    my_article = paginator.get_page(page)
    count = user.article_set.all().count()
    following = user.is_following.all().count()
    followers = user.profile.followers.all().count()
    context = {
                'user': user,
                'my_article': my_article,
                'count': count,
                'following': following,
                'followers': followers
                }
    return render(request, 'articles/users_detail.html', context)


def users_detail_comments(request, pk):
    article_com = Article.objects.get(id=pk)
    comments = Comment.objects.filter(post=article_com).order_by('-created_date')
    paginator = Paginator(comments, 10)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    context = {
                'comments': comments
               }
    return render(request, 'articles/users_detail_comments.html', context)


def users_detail_liked(request, pk):
    article_title = Article.objects.get(id=pk)
    liked_users = article_title.like.all().order_by('?')
    paginator = Paginator(liked_users, 10)
    page = request.GET.get('page')
    liked_users = paginator.get_page(page)
    context = {
                'liked_users': liked_users
                }
    return render(request, 'articles/users_detail_like.html', context)


#@login_required(login_url="/accounts/login/")
def article_edit(request, pk):
    if id:
        post = get_object_or_404(Article, pk=pk)
        if post.author != request.user:
            #return HttpResponseForbidden() #default
            raise PermissionDenied
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


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    articles_category = category.article_set.all().order_by('-date')
    paginator = Paginator(articles_category, 24)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'articles/category_detail.html', context)


class UserPostListView(ListView):
    model = Article
    template_name = 'articles/user_post_list.html'
    context_object_name = 'articles'
    paginate_by = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super().get_context_data(**kwargs)
        context.update({
            'user': user,
            'following': user.is_following.all().count(),
            'followers': user.profile.followers.all().count(),
            'bio': user.profile.bio,
            'website': user.profile.website,
            'count': user.article_set.all().count()
        })
        articles = Article.objects.filter(author=user).order_by('-date')
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date')


class Gallery(ListView):
    model = Article
    template_name = 'articles/article_photo_gallery.html'
    paginate_by = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category_list': Category.objects.order_by('category_name'),
            'categories': Category.objects.annotate(
                num_article=Count('article', filter=Q())
            ),
        })
        articles = Article.objects.all().order_by('-date')
        return context

    def get_queryset(self):
        return Article.objects.all().order_by('-date')


class ArticleOrderedByLikes(ListView):
    model = Article
    template_name = 'articles/article_ordered_by_likes.html'
    context_object_name = 'articles'
    paginate_by = 9

    def get_queryset(self):
        return Article.objects.annotate(like_count=Count('like')).order_by('-like_count')