from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy

from .models import Article


class ArticlesListView(ListView):
    """
    Articles ListView
    """
    # template_name = 'blogapp/article_list.html'
    queryset = Article.objects.defer("content").select_related("author", "category").prefetch_related("tags").order_by('-pub_date')
    # rename context_data name, default name object_list which can be used in a template
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    template_name = "blogapp/article_details.html"
    model = Article


# RSS articles
class LatestArticlesFeed(Feed):
    """
    RSS Articles View
    """
    title = "Blog articles (latest)"
    description = 'Updates on changes and addition blog articles'
    link = reverse_lazy("blogapp:articles_list")

    def items(self):
        return (Article.objects
                .defer("content")
                .select_related("author", "category")
                .prefetch_related("tags")
                .order_by('-pub_date')[:5]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]

    # add to model Article as method
    # def item_link(self, item: Article):
    #     return reverse('blogapp:article_details', kwargs={'pk': item.pk})