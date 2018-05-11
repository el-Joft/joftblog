from django.contrib import admin
from posts.models import Post, Category

# Register your models here.

class PostAdminModel(admin.ModelAdmin):
# ...
    list_display = ('title', 'created', 'allow_comments','modified')
    list_display_links = ["modified"]
    list_filter  = ["modified", "created"]
    list_editable   = ["title"]
    search_fields   = ["title", ]
    class Meta:
        model = Post

admin.site.register(Post, PostAdminModel)
admin.site.register(Category)