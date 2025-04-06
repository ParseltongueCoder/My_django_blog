from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)  # A text field for the post's title.
    content = models.TextField()              # A field for the post's content.
    date_posted = models.DateTimeField(auto_now_add=True)  # Automatically set the date/time when a post is created.
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Associates the post with a user.

    objects = models.Manager()

    def __str__(self):
        return self.title  # This returns the title when the object is printed.

    def get_absolute_url(self):
        # Returns the URL to access a detail view of this post.
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Link to the corresponding post.
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the comment.
    content = models.TextField()  # The comment text.
    date_posted = models.DateTimeField(auto_now_add=True)  # The date/time when the comment was made.

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


class HeroBanner(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero_banners/')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return self.title
