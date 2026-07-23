from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.base import View

from accounts.models import Profile
from articles.models import Article
from .forms import UserCreationForms, ContactForm, UserUpdateForm, ProfileUpdateForm
from django.utils import timezone 
from django.contrib.auth import get_user_model


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('articles:list')
    else:
        form = UserCreationForms()
        
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('articles:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('articles:list')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            # clear処理
            profile_instance = p_form.instance
            if request.POST.get('image-clear'):
                profile_instance.image.delete(save=False)
                profile_instance.image = "default.png"
            if request.POST.get('bg-clear'):
                profile_instance.bg.delete(save=False)
                profile_instance.bg = None
            # ここまで

            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)


def Success(request):
    return render(request, 'accounts/success.html')


def Contact(request):
    Contact_Form = ContactForm
    if request.method == 'POST':
        form = Contact_Form(data=request.POST)

        if form.is_valid():
            contact_name    = request.POST.get('contact_name')
            contact_email   = request.POST.get('contact_email')
            contact_message = request.POST.get('message')
            template        = get_template('accounts/contact_form.txt')
            context = {
                'contact_name'   : contact_name,
                'contact_email'  : contact_email,
                'contact_message': contact_message,
            }

            content = template.render(context)

            email = EmailMessage(
                'New contact form Localthings',
                content,
                'Local things' + '',
                [config('EMAIL_HOST_USER')],
                headers={'Reply To': contact_email}
            )

            email.send()
            return redirect('accounts:success')
    return render(request, 'accounts/contact.html', {'form': Contact_Form})


def Delete_user(self):
    self.user.delete()
    return redirect('articles:list')


@login_required
def user_is_following(request, username):
    target_user   = get_object_or_404(User, username=username)
    following_qs  = target_user.following_users.all().order_by('id')

    paginator     = Paginator(following_qs, 20)
    page          = request.GET.get('page')
    following_page = paginator.get_page(page)

    # ✅ ログインユーザーがフォローしている人
    is_following_set = set()
    if request.user.is_authenticated:
        is_following_set = set(request.user.following_users.all())

    context = {
        'user'             : target_user,
        'following_page'   : following_page,
        'is_following_set' : is_following_set,
    }
    return render(request, 'accounts/is_following.html', context)


@login_required
def user_followers(request, username):
    # 対象ユーザー（見られている人）を取得
    target_user = get_object_or_404(User, username=username)

    # followers: このユーザーをフォローしている User の一覧（ManyToMany）
    follower_users = target_user.profile.followers.all().order_by('id')

    paginator = Paginator(follower_users, 20)
    page      = request.GET.get('page')
    followers = paginator.get_page(page)

    # ✅ フォロー中のユーザーセット（自分がフォローしている人）
    is_following_set = set()
    if request.user.is_authenticated:
        is_following_set = set(request.user.following_users.all())

    context = {
        'user'            : target_user,
        'followers'       : followers,
        'is_following_set': is_following_set,
    }
    return render(request, 'accounts/followers.html', context)


class PasswordReset(PasswordResetView):
    subject_template_name = 'accounts/mail_template/reset/subject.txt'
    email_template_name   = 'accounts/mail_template/reset/message.txt'
    template_name         = 'accounts/password_reset.html'
    success_url           = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url   = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    login_url     = '/accounts/login/'
    template_name = 'accounts/user.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username)

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            raise Http404
        else:
            context      = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
            user         = context['user']
            is_following = False

            if user.profile in self.request.user.following_users.all():
                is_following = True

            context['is_following'] = is_following
            return context


class ProfileFollowToggle(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        username_to_toggle     = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success'           : True,
                'is_following'      : is_following,
                'followers_count'   : profile_.followers.count(),
                'following_count'   : profile_.user.following_users.count(),  
                'my_following_count': request.user.following_users.count(), 
            })

        return redirect(f"/accounts/{profile_.user.username}")



class UserFollowingFeedView(View):
    def format_custom_date_style(self, date, now):
        delta = now - date
        if delta.days < 7:
            return f"{delta.days}日前" if delta.days > 0 else "今日"
        else:
            return date.strftime("%-m月%-d日")  # Linux/Mac

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'articles/article_list_new.html', {})

        User = get_user_model()
        user = User.objects.get(id=request.user.id)  # ✅ 最新ユーザーで更新

        post_articles       = Article.objects.all()
        order_like_articles = post_articles.annotate(like_count=Count('like')).order_by('-like_count')[:5]
        count               = user.article_set.count()

        # ✅ フォロー中ユーザーのID取得
        is_following_user_ids = list(user.following_users.values_list('user__id', flat=True))
        following_users       = set(is_following_user_ids)

        # ✅ 記事取得 & カスタム属性追加
        qs  = list(Article.objects.filter(author__id__in=following_users).order_by('-date'))
        now = timezone.now()
        for article in qs:
            article.display_date = self.format_custom_date_style(article.date, now)
            article.is_following = article.author.id in following_users

        # ✅ paginator処理
        paginator = Paginator(qs, 10)
        page      = request.GET.get('page')
        articles  = paginator.get_page(page)

        context = {
            'articles'           : articles,
            'count'              : count,
            'order_like_articles': order_like_articles,
            'users'              : Profile.objects.all().order_by('?')[:4],
        }
        return render(request, 'accounts/user_new_following.html', context)