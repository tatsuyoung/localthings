from django.contrib import admin
from .models import Article, Comment, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    readonly_fields = ['date']
    search_fields = ['title', 'body']
    list_filter = ['category']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)