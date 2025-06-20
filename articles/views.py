import json
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from notifications.signals import notify

from accounts.models import Profile
from .models import Comment, Category
from .models import Article, ArticleImage
from. import forms

from django.forms import inlineformset_factory
from .forms import CreateArticle, ArticleImageForm

from django.http import HttpResponseServerError
import logging
logger = logging.getLogger(__name__)

def article_list(request):
    users               = Profile.objects.all().order_by('?')[:4]
    articles_list       = Article.objects.all().order_by('-date')
    order_like_articles = articles_list.annotate(like_count=Count('like')).order_by('?')[:5]
    paginator           = Paginator(articles_list, 24)
    page                = request.GET.get('page')
    articles            = paginator.get_page(page)

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


def article_detail(request, pk):
    users               = Profile.objects.all().order_by('?')[:4]
    articles_list       = Article.objects.all().order_by('-date')
    order_like_articles = articles_list.annotate(like_count=Count('like')).order_by('?')[:5]
    article             = Article.objects.get(pk=pk)
    return render(request, 'articles/article_detail_new.html',
                  {'article': article,
                   'order_like_articles': order_like_articles,
                   'users': users
                   }
                  )

@login_required(login_url="/accounts/login/")
def article_create(request, num_images=5):
    try:
        if request.method == 'POST':
            form = forms.CreateArticle(request.POST)
            files = request.FILES.getlist('images')
            logger.info(f"FILES: {[f.name for f in files]}")
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()

                for i, image in enumerate(files):
                    if i >= num_images:
                        break
                    ArticleImage.objects.create(article=instance, image=image)

                return redirect('articles:list')
            else:
                logger.error(f"Form errors: {form.errors}")
                return render(request, 'articles/article_create.html', {'form': form})

        else:
            form = forms.CreateArticle()
            return render(request, 'articles/article_create.html', {'form': form})

    except Exception as e:
        logger.exception("Error during article_create")
        return HttpResponseServerError("Internal Server Error")


ArticleImageFormSet = inlineformset_factory(
        Article,
        ArticleImage,
        form=ArticleImageForm,
        extra=1,  # 新規に追加できるフォーム数
        can_delete=True  # 削除チェックボックスを有効化
    )

@login_required(login_url="/accounts/login/")
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = CreateArticle(request.POST, request.FILES, instance=article)
        formset = ArticleImageFormSet(request.POST, request.FILES, instance=article)

        if form.is_valid() and formset.is_valid():
            article = form.save()
            formset.save()  # ← これだけでOK！
            return redirect('articles:detail', pk=article.pk)
    else:
        form = CreateArticle(instance=article)
        formset = ArticleImageFormSet(instance=article)

    return render(request, 'articles/article_edit.html', {
        'form': form,
        'formset': formset,
        'article': article,
    })


@require_POST
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return redirect('articles:list')


@login_required(login_url="/accounts/login/")
@require_POST
def article_comment(request, pk):
    users               = Profile.objects.all().order_by('?')[:4]
    articles_list       = Article.objects.all().order_by('-date')
    order_like_articles = articles_list.annotate(like_count=Count('like')).order_by('?')[:5]
    article_com         = Article.objects.get(id=pk)
    comments            = Comment.objects.filter(post=article_com).order_by('created_date')
    current_user        = request.user

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment        = form.save(commit=False)
            comment.post   = article_com
            comment.author = request.user
            comment.save()
    else:
        form = forms.CommentForm()
    context = {
                'article'            : article_com,
                'form'               : form,
                'comments'           : comments,
                'current_user'       : current_user,
                'order_like_articles': order_like_articles,
                'users'              : users
               }
    return render(request, 'articles/article_detail_new.html', context)


@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('articles:list')


@login_required(login_url="/accounts/login/")
def book_mark_list(request):
    user         = request.user
    my_book_mark = user.book_mark.all().order_by('-date')
    context      = {
        'my_book_mark': my_book_mark
    }
    return render(request, 'articles/article_book_mark.html', context)


@require_POST
def book_mark(request, book_mark_id):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Please log in.'}, status=403)

    if request.method == 'POST':
        user         = request.user
        title        = request.POST.get('title', None)
        article      = get_object_or_404(Article, title=title, id=book_mark_id)

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
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Please log in.'}, status=403)

    user    = request.user
    title   = request.POST.get('title', None)
    article = get_object_or_404(Article, title=title, id=like_id)

    if article.like.filter(id=user.id).exists():
        article.like.remove(user)
        message = 'いいねを取り消しました。'
    else:
        article.like.add(user)
        url     = article.get_url()
        message = 'いいねしました。'
        notify.send(
            user,
            recipient=article.author,
            verb=f'さんが、あなたの記事にいいねしました。{article.title}',
            action_object=article,
            url=url
        )

    context = dict(likes_count=article.total_likes, message=message)
    return JsonResponse(context)


def users_detail(request, pk):
    users               = Profile.objects.all().order_by('?')[:4]
    articles_list       = Article.objects.all().order_by('-date')
    order_like_articles = articles_list.annotate(like_count=Count('like')).order_by('?')[:5]
    current_user        = request.user
    user                = get_object_or_404(User, pk=current_user.pk)
    my_article          = user.article_set.all().order_by('-date')
    paginator           = Paginator(my_article, 9)
    page                = request.GET.get('page')
    articles            = paginator.get_page(page)
    count               = user.article_set.all().count()
    following           = user.is_following.all().count()
    followers           = user.profile.followers.all().count()

    context = {
                'user': user,
                'articles': articles,
                'count': count,
                'following': following,
                'followers': followers,
                'order_like_articles': order_like_articles,
                'users': users
                }
    return render(request, 'articles/users_detail_new.html', context)


def users_detail_comments(request, pk):
    article_com = Article.objects.get(id=pk)
    comments    = Comment.objects.filter(post=article_com).order_by('-created_date')
    paginator   = Paginator(comments, 10)
    page        = request.GET.get('page')
    comments    = paginator.get_page(page)
    context = {
                'comments': comments
               }
    return render(request, 'articles/users_detail_comments.html', context)


def users_detail_liked(request, pk):
    article_title = Article.objects.get(id=pk)
    liked_users   = article_title.like.all().order_by('?')
    paginator     = Paginator(liked_users, 10)
    page          = request.GET.get('page')
    liked_users   = paginator.get_page(page)
    context = {
                'liked_users': liked_users
                }
    return render(request, 'articles/users_detail_like.html', context)


def category_detail(request, pk):
    category          = get_object_or_404(Category, pk=pk)
    articles_category = category.article_set.all().order_by('-date')
    paginator         = Paginator(articles_category, 24)
    page              = request.GET.get('page')
    articles          = paginator.get_page(page)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'articles/category_detail.html', context)


class UserPostListView(ListView):
    model               = Article
    template_name       = 'articles/user_post_list.html'
    context_object_name = 'articles'
    paginate_by         = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        _user               = get_object_or_404(User, username=self.kwargs.get('username'))
        users               = Profile.objects.all().order_by('?')[:4]
        articles_list       = Article.objects.all().order_by('-date')
        order_like_articles = articles_list.annotate(like_count=Count('like')).order_by('?')[:5]
        context = super().get_context_data(**kwargs)
        context.update({
            'User'     : _user,
            'following': _user.is_following.all().count(),
            'followers': _user.profile.followers.all().count(),
            'bio'      : _user.profile.bio,
            'website'  : _user.profile.website,
            'count'    : _user.article_set.all().count(),
            'users'    : users,
            'order_like_articles': order_like_articles
        })
        articles = Article.objects.filter(author=_user).order_by('-date')
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date')


class Gallery(ListView):
    model         = Article
    template_name = 'articles/article_photo_gallery.html'
    paginate_by   = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category_list': Category.objects.order_by('category_name'),
            'categories': Category.objects.annotate(
                num_article=Count('article', filter=Q())
            ),
        })
        #articles = Article.objects.all().order_by('-date')
        return context

    def get_queryset(self):
        return Article.objects.filter(images__isnull=False).distinct().order_by('-date')


class ArticleOrderedByLikes(ListView):
    model               = Article
    template_name       = 'articles/article_ordered_by_likes.html'
    context_object_name = 'articles'
    paginate_by         = 9

    def get_queryset(self):
        return Article.objects.annotate(like_count=Count('like')).order_by('-like_count')