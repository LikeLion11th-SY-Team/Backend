from django.contrib import admin
from . import models

class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0
    min_num = 0
    max_num = 20
    readonly_fields = ['created_at']
    verbose_name = '댓글'
    verbose_name_plural = '댓글'

@admin.register(models.Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_at','view_count','writer']
    search_fields = ['id','writer__nickname']
    
    readonly_fields = ['created_at']
    inlines = [CommentInline]