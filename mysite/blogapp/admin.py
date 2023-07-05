from django.contrib import admin
from .models import Article, Tag, Category, Author
# Register your models here.


class TagInline(admin.TabularInline):
    model = Article.tags.through


class ArticleInline(admin.TabularInline):
    model = Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]

    list_display = (
        "pk",
        "verbose_title",
        "content",
        "pub_date",
        "author_verbose",
    )

    list_display_links = ("pk", 'verbose_title',)

    def get_queryset(self, request):
        return Article.objects.select_related("author", "category").prefetch_related("tags")

    def author_verbose(self, obj: Article) -> str:
        return obj.author.name

    def verbose_title(self, obj: Article) -> str:
        if len(obj.title) < 20:
            return obj.title
        return obj.title[:20] + "..."


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]

    list_display = (
        "pk",
        "name",
    )

    ordering = (
        "name",
    )

    list_display_links = (
        "pk",
        "name",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        # ArticleInline,
    ]

    list_display = (
        "pk",
        "name",
    )

    ordering = (
        "name",
    )

    list_display_links = (
        "name",
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        # ArticleInline,
    ]

    list_display = (
        "pk",
        "name",
        "bio",
    )

    ordering = (

    )

    list_display_links = (
        "pk",
        "name",
    )