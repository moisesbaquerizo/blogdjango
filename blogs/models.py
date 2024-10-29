from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    overview = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    categorias = models.ManyToManyField('Category', related_name='posts')
    featured = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("blogs:post", kwargs={"slug": self.slug})

    @property
    def average_rating(self):
        return self.ratings.aggregate(average=Avg('stars'))['average'] or 0

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse("blogs:category", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(max_length=1000, help_text="Ingrese comentario")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        len_title = 15
        if len(self.content) > len_title:
            return self.content[:len_title] + '....'
        return self.content

class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.stars} stars for {self.post} by {self.user}"
