from django.contrib import admin
from .models import UserProfile, Goal, BlogPost

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')  # Removed 'location' because it doesn’t exist
    search_fields = ('user__username',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category')  # Removed 'created_at' to fix error
    search_fields = ('title', 'user__username')
    list_filter = ('category',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
