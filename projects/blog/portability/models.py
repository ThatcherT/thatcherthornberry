from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.TextField()
    subheading = models.TextField()
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
