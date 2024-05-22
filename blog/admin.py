from django.contrib import admin
from .models import Post,Category,Comment

admin.site.register(Category)
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','publish','category','author']
    list_filter = ['publish','category','status']
    prepopulated_fields = {'slug':('title',)}
    ordering = ['status','publish']