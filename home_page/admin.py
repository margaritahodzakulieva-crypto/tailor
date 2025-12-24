from django.contrib import admin
from .models import Profile, Post


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image','about')
    search_fields = ('user', 'image','about')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_image', 'post_title', 'post_description', 'post_file', 'date_posted')
    search_fields = ('user', 'post_title', 'post_description', 'post_file', 'date_posted')
    list_filter = ('user', 'post_title', 'date_posted')