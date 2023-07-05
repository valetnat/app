from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Author(models.Model):
    """
    Model Author. Describe author of article
    """
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=False, blank=True)

    def __str__(self):
        return f"Author (pk={self.pk}, name={self.name!r})"


class Category(models.Model):
    """
    Model Category. Describe category of article
    """
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=40, db_index=True)

    def __str__(self):
        return f"Category (pk={self.pk}, name={self.name!r})"


class Tag(models.Model):
    """
    Model Tag. Describe tag of article
    """

    class Meta:
        pass

    name = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return f"Tag (pk={self.pk}, name={self.name!r})"


class Article(models.Model):
    """
    Model Article.
    """
    title = models.CharField(max_length=200)
    content = models.TextField(blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')

    def get_absolute_url(self):
        return reverse('blogapp:article_details', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Article (pk={self.pk}, name={self.title!r})"
