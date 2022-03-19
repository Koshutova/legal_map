from django.contrib import admin

from legal_map.articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'picture', 'author_name', 'article_text', 'created',)
    readonly_fields = ('created', )


admin.site.register(Article, ArticleAdmin)
