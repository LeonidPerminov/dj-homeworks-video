from django.db import models
from django.core.exceptions import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    published_at = models.DateTimeField()
    tags = models.ManyToManyField(Tag, through='Scope', related_name='articles')

    def __str__(self):
        return self.title


class Scope(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('tag', 'article')

    def __str__(self):
        return f"{self.article.title} — {self.tag.name} ({'main' if self.is_main else 'extra'})"
