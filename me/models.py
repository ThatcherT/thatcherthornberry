from django.db import models

# Create your models here.

class Review(models.Model):
    title = models.CharField(max_length=200)
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=55)
    relation = models.CharField(max_length=55)

    @property
    def unrating(self):
        return 5 - self.rating

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_at']
    