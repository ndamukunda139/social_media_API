from django.contrib import admin

# Register post and comment models in admin
from .models import Post, Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'content','created_at']
    search_fields = ['title', 'content']
    list_filter = ['created_at', 'author']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'content','created_at']
    search_fields = ['content']
    list_filter = ['created_at', 'author']