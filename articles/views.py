import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage

from django.db.models import Subquery
from django.db.models import OuterRef, Exists
from django.db.models import Q, Count

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.http import require_POST
from django.views.generic import ListView
from notifications.signals import notify

from accounts.models import Profile
from .models import Comment, Category
from .models import Article, ArticleImage

from. import forms
from django.forms import inlineformset_factory
from .forms import CreateArticle, ArticleImageForm
from django.forms.models import modelformset_factory

import logging
logger = logging.getLogger(__name__)

from django.urls import reverse
from django.utils import timezone
from .utils import format_custom_date_style  # ← 日付フォーマット関数
from django.template.loader import render_to_string

from django.http import Http404

# Story
from stories.models import Story, StoryRead
from collections import OrderedDict




# Articles

def article_search_partial(request):
    return render(request, 'articles/article_search_partial.html')

def get_article_context(article):
    articles_list        = Article.objects.all().order_by('-date')
    order_like_articles  = articles_list.annotate(like_count=Count('like')).order_by('?')[:5]
    users                = Profile.objects.all().order_by('?')[:4]
    now                  = timezone.now()
    article.display_date = format_custom_date_style(article.date, now)
    comments             = Comment.objects.filter(post=article).order_by('created_date')
    form                 = forms.CommentForm()
    current_user         = article.author  # または request.user（後で上書き）
    now = timezone.now()
    for comment in comments:
        comment.display_date = format_custom_date_style(comment.created_date, now)
    return {
        'article'            : article,
        'order_like_articles': order_like_articles,
        'users'              : users,
        'comments'           : comments,
        'form'               : form,
        'current_user'       : current_user,
    }

def article_search(request):
    query = request.GET.get("q", "")
    articles = Article.objects.filter(
        Q(title__icontains=query) |
        Q(body__icontains=query)
    ).order_by('-date') if query else Article.objects.none()

    paginator   = Paginator(articles, 10)
    page_number = request.GET.get("page", 1)
    page_obj    = paginator.get_page(page_number)

    # ✅ display_date をつける
    now = timezone.now()
    for article in page_obj:
        article.display_date = format_custom_date_style(article.date, now)

    # ✅ 各 author の followers / following 数を dict に格納
    followers_count = {}
    following_count = {}

    if request.user.is_authenticated:
        for article in page_obj:
            followers_count[article.author.username]  = article.author.profile.followers.count()
            following_count[article.author.username]  = article.author.following_users.count()

    # follow
    is_following_set = set()
    if request.user.is_authenticated:
        is_following_set = set(request.user.following_users.all())

    # ✅ author_count_dict を計算
    author_ids = [article.author.id for article in page_obj]
    author_article_counts = Article.objects.filter(author__id__in=author_ids) \
                                        .values('author') \
                                        .annotate(count=Count('id'))

    author_count_dict = {item['author']: item['count'] for item in author_article_counts}

    # ✅ コメント & フォーム
    article_comment_data = {}
    for article in page_obj:
        all_comments = Comment.objects.filter(post=article).order_by('created_date')
        article_comment_data[article.id] = {
            'comments': all_comments,
            'form'    : forms.CommentForm(),
        }

    context = {
        "articles"            : page_obj,
        "query"               : query,
        "article_comment_data": article_comment_data,
        "author_count_dict"   : author_count_dict,
        'followers_count'     : followers_count,
        'following_count'     : following_count,
        "is_following_set"    : is_following_set,
        "view_name"           : "search", 
    }

    return render(request, "articles/article_search.html", context)


def article_list(request):
    users               = Profile.objects.all().order_by('?')[:4]
    articles_list       = Article.objects.all().order_by('-date')
    order_like_articles = articles_list.annotate(like_count=Count('like')).order_by('?')[:5]
    page_number         = request.GET.get("page", 1)

    paginator = Paginator(articles_list, 10)
    page_obj  = paginator.get_page(page_number)

    # ✅ 日付表示を整形して付加
    now = timezone.now()
    for article in page_obj:
        article.display_date = format_custom_date_style(article.date, now)

        if request.user.is_authenticated:
            following_user_ids = set(request.user.following_users.values_list('id', flat=True))
            for article in page_obj:
                article.is_following = article.author.id in following_user_ids
        else:
            for article in page_obj:
                article.is_following = False  # 未ログインなら全部False
    # ✅ 各 author の followers / following 数を dict に格納
    followers_count = {}
    following_count = {}

    if request.user.is_authenticated:
        for article in page_obj:
            followers_count[article.author.username]  = article.author.profile.followers.count()
            following_count[article.author.username]  = article.author.following_users.count()

    # follow
    is_following_set = set()
    if request.user.is_authenticated:
        is_following_set = set(request.user.following_users.all())

    # ✅ 各 author の記事数を取得 → {user_id: 投稿数} の dict に
    author_ids = [article.author.id for article in page_obj]
    author_article_counts = Article.objects.filter(author__id__in=author_ids) \
                                        .values('author') \
                                        .annotate(count=Count('id'))

    author_count_dict = {item['author']: item['count'] for item in author_article_counts}

    # ✅ Stories（自分 + フォロー中のユーザーのStoryのみ）
    story_users    = []
    read_stories   = []
    unread_stories = []

    if request.user.is_authenticated:
        now = timezone.now()

        # 自分のストーリー（有効期限内）
        own_story = Story.objects.filter(
            user=request.user,
            expires_at__gt=now
        ).order_by('-created_at').first()

        if own_story:
            own_story.is_read = False  # 自分のストーリーは未読扱い
            unread_stories.append(own_story)

        # フォロー中のユーザーのID
        following_user_ids = Profile.objects.filter(
            followers=request.user
        ).values_list('user__id', flat=True)

        # フォロー中のユーザーの有効なストーリー
        other_stories_qs = Story.objects.filter(
            user__id__in=following_user_ids,
            expires_at__gt=now
        ).select_related('user').prefetch_related('reads').order_by('user_id', '-created_at')

        # ✅ 自分が読んだストーリーのIDをまとめて取得
        read_story_ids = set(
            StoryRead.objects.filter(user=request.user).values_list('story_id', flat=True)
        )

        seen_user_ids = {request.user.id}  # 自分の分はスキップ対象

        for s in other_stories_qs:
            if s.user.id in seen_user_ids:
                continue

            seen_user_ids.add(s.user.id)
            s.is_read = s.id in read_story_ids  # ✅ フラグ付け

            if s.is_read:
                read_stories.append(s)
            else:
                unread_stories.append(s)

        # 最終的な表示用リスト
        story_users = unread_stories + read_stories
    

    # ✅ 各記事に全コメントと1つのフォームを付加
    now = timezone.now()
    article_comment_data = {}
    for article in page_obj:
        all_comments = Comment.objects.filter(post=article).order_by('created_date')
        # 各コメントに display_date を追加
        for comment in all_comments:
            comment.display_date = format_custom_date_style(comment.created_date, now)
            
        article_comment_data[article.id] = {
            'comments': all_comments,
            'form'    : forms.CommentForm(),
        }
    context = {
        'articles'            : page_obj,
        'article_comment_data': article_comment_data,
        'author_count_dict'   : {
            item['author']: item['count']
            for item in Article.objects.filter(author__in=[a.author for a in page_obj])
                .values('author')
                .annotate(count=Count('id'))
        },
        'view_name': 'list',
    }

    # ✅ Ajaxの場合はJSONで返す
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context.update({
        'followers_count' : followers_count,
        'following_count' : following_count,
        'is_following_set': is_following_set,
        })
        html = render_to_string("articles/partial_article_card_list.html", context, request=request)
        return JsonResponse({
            'html'    : html,
            'has_next': page_obj.has_next(),
        })

    # ✅ context
    return render(request, 'articles/article_list_new.html', {
        'articles'            : page_obj,
        'order_like_articles' : order_like_articles,
        'users'               : users,
        'author_count_dict'   : author_count_dict,
        'article_comment_data': article_comment_data,
        'followers_count'     : followers_count,
        'following_count'     : following_count,
        'is_following_set'    : is_following_set,   
        'view_name'           : 'list',
        'story_users'         : story_users,
    })


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = get_article_context(article)
    context['current_user'] = request.user
    context['view_name']    = 'detail'

    return render(request, 'articles/article_detail_new.html', context)


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
                instance.date   = timezone.now()
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
        can_delete=True,  # 削除チェックボックスを有効化
        max_num=5,  # 最大数を制限
    )

@login_required(login_url="/accounts/login/")
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form    = CreateArticle(request.POST, request.FILES, instance=article)
        formset = ArticleImageFormSet(request.POST, request.FILES, instance=article)

        if form.is_valid() and formset.is_valid():
            article = form.save()

            images = formset.save(commit=False)
            for image in images:
                image.article = article
                image.save()

            for deleted_form in formset.deleted_objects:
                deleted_form.delete()

            formset.save_m2m()  # 多対多があれば（なければ省略してOK）

            return redirect('articles:detail', pk=article.pk)

        else:
            print("❌ formまたはformsetが無効")
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)

    else:
        form    = CreateArticle(instance=article)
        formset = ArticleImageFormSet(instance=article)

    return render(request, 'articles/article_edit.html', {
        'form'   : form,
        'formset': formset,
        'article': article,
    })


@require_POST
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return redirect('articles:list')


# Comment
@login_required(login_url="/accounts/login/")
@require_POST
def article_comment(request, pk):
    article = get_object_or_404(Article, id=pk)

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment        = form.save(commit=False)
            comment.post   = article
            comment.author = request.user
            comment.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                comments = Comment.objects.filter(post=article).order_by('created_date')
                now = timezone.now()
                for comment in comments:
                    comment.display_date = format_custom_date_style(comment.created_date, now)

                html = render_to_string('articles/partial_comment_list.html', {
                    'comments' : comments,
                    'article'  : article,
                    'request'  : request,
                    'view_name': 'list',
                })
                return JsonResponse({'html': html})
            return redirect('articles:detail', pk=article.pk)  # ✅ POST後にリダイレクト

    # POST でない or フォームエラー
    context                 = get_article_context(article)
    context['form']         = form  # エラーのあるフォームで上書き
    context['current_user'] = request.user
    return render(request, 'articles/article_detail_new.html', context)


@require_POST
@login_required
def delete_comment_ajax(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        return JsonResponse({'error': '削除権限がありません'}, status=403)

    article = comment.post
    comment.delete()

    comments = Comment.objects.filter(post=article).order_by('created_date')
    html = render_to_string('articles/partial_comment_list.html', {
        'comments': comments,
        'article' : article,
        'request' : request,
    }, request=request)
    return JsonResponse({'html': html})

# Book mark
@login_required(login_url="/accounts/login/")
def book_mark_list(request):
    user         = request.user
    my_book_mark = user.book_mark.all().order_by('-date')
    context      = {
        'my_book_mark': my_book_mark
    }
    return render(request, 'articles/article_book_mark.html', context)


@require_POST
def book_mark(request, article_id):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Please Login'}, status=403)

    article = get_object_or_404(Article, id=article_id)
    user = request.user

    if article.book_mark.filter(id=user.id).exists():
        article.book_mark.remove(user)
        message = 'Book Markから外しました。'
    else:
        article.book_mark.add(user)
        message = 'Book Markしました。'

    return JsonResponse({'message': message})

# Liked
@require_POST
def like_button(request, like_id):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Please Login.'}, status=403)

    user = request.user
    article = get_object_or_404(Article, id=like_id)

    if article.like.filter(id=user.id).exists():
        article.like.remove(user)
    else:
        article.like.add(user)
        url = article.get_url()
        notify.send(
            user,
            recipient=article.author,
            verb=f'さんが、あなたのpostにいいね!しました。{article.title}',
            action_object=article,
            data={'url': url} 
        )

    return JsonResponse({'likes_count': article.total_likes})


class ArticleOrderedByLikes(ListView):
    model               = Article
    template_name       = 'articles/article_ordered_by_likes.html'
    context_object_name = 'articles'
    paginate_by         = 9

    def get_queryset(self):
        return Article.objects.annotate(like_count=Count('like')).order_by('-like_count')

    def format_custom_date_style(self, date, now):
        delta = now - date
        if delta.days < 7:
            return f"{delta.days}日前" if delta.days > 0 else "今日"
        else:
            return date.strftime("%-m月%-d日")  # Mac/Linux（Windowsなら %#m）

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        for article in context['articles']:
            article.display_date = self.format_custom_date_style(article.date, now)
        return context


# User
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
    following           = user.following_users.all().count()
    followers           = user.profile.followers.all().count()
    # ✅ 各記事に display_date を追加
    now = timezone.now()
    for article in articles:
        article.display_date = format_custom_date_style(article.date, now)

    context = {
                'user'     : user,
                'articles' : articles,
                'count'    : count,
                'following': following,
                'followers': followers,
                'order_like_articles': order_like_articles,
                'users': users
                }
    return render(request, 'articles/users_detail_new.html', context)


def users_detail_comments(request, pk):
    article_com = Article.objects.get(id=pk)
    comments    = Comment.objects.filter(post=article_com).order_by('-created_date')
    paginator   = Paginator(comments, 24)
    page        = request.GET.get('page')
    comments    = paginator.get_page(page)
    context = {
                'comments': comments
               }
    return render(request, 'articles/users_detail_comments.html', context)


def users_detail_liked(request, pk):
    article_title = Article.objects.get(id=pk)
    liked_users   = article_title.like.all().order_by('?')
    paginator     = Paginator(liked_users, 48)
    page          = request.GET.get('page')
    liked_users   = paginator.get_page(page)
    context = {
                'liked_users': liked_users
                }
    return render(request, 'articles/users_detail_like.html', context)


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
        articles            = Article.objects.filter(author=_user).order_by('-date')

        context = super().get_context_data(**kwargs)

        context.update({
            'User'     : _user,
            'following': _user.following_users.all().count(), 
            'followers': _user.profile.followers.all().count(),
            'bio'      : _user.profile.bio,
            'website'  : _user.profile.website,
            'count'    : _user.article_set.all().count(),
            'users'    : users,
            'order_like_articles': order_like_articles
        })
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date')


# Category
def category_detail(request, pk):
    category          = get_object_or_404(Category, pk=pk)
    articles_category = category.article_set.all().order_by('-date')
    paginator         = Paginator(articles_category, 24)
    page              = request.GET.get('page')
    articles          = paginator.get_page(page)
    # ✅ 日付表示を整形して付加
    now = timezone.now()
    for article in articles:
        article.display_date = format_custom_date_style(article.date, now)
        
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'articles/category_detail.html', context)


# Gallery
def gallery(request):
    page = request.GET.get("page", 1)

    articles = (
        Article.objects
        .filter(images__isnull=False)
        .exclude(images__image__icontains="No-image.png")
        .order_by("-date")
        .distinct()
    )

    paginator = Paginator(articles, 11)

    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"html": "", "has_next": False})
        else:
            raise Http404(f"無効なページです ({page})")

    # ✅ カテゴリを追加
    categories = Category.objects.all().annotate(num_article=Count("article"))

    context = {
        "articles"  : page_obj,
        "page_obj"  : page_obj,
        "categories": categories
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("articles/partial_gallery_card_list.html", context, request=request)
        return JsonResponse({
            "html"    : html,
            "has_next": page_obj.has_next()
        })

    return render(request, "articles/article_photo_gallery.html", context)


def article_by_tag(request, tag):
    page_number = int(request.GET.get("page", 1))

    # ✅ ArticleImage が存在するかどうかのサブクエリ
    has_images = ArticleImage.objects.filter(article=OuterRef('pk'))

    # ✅ まず、画像付きかつタグ一致する Article の「IDリスト」を抽出
    matching_ids_subquery = Article.objects.annotate(
        has_images=Exists(has_images)
    ).filter(
        body__icontains=f'#{tag}',
        has_images=True
    ).order_by('-date').values('id')

    # ✅ それらの ID に一致する Article を順序付きで取得
    articles  = Article.objects.filter(id__in=Subquery(matching_ids_subquery)).order_by('-date')

    paginator = Paginator(articles, 10)
    page_obj  = paginator.get_page(page_number)

    # print("[AJAX]" if request.headers.get("x-requested-with") == "XMLHttpRequest" else "[HTML]", "page_obj IDs:", [a.id for a in page_obj])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("articles/partial_article_tag_items_list.html", {"articles": page_obj})
        article_data = {
            str(article.id): {
                "images"        : [img.image.url for img in article.images.all()],
                "userIcon"      : article.author.profile.image.url,
                "userName"      : article.author.username,
                "body"          : article.body.replace('\n', '<br>'),
                "userProfileUrl": reverse('articles:user-posts', args=[article.author.username])
            }
            for article in page_obj
        }
        return JsonResponse({
            "html"        : html,
            "has_next"    : page_obj.has_next(),
            "article_data": article_data,
        })

    return render(request, 'articles/article_by_tag.html', {
        'tag'     : tag,
        'articles': page_obj,
        'has_next': page_obj.has_next()
    })