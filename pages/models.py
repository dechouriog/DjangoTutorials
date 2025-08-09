from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="photos/")  # Se guardará en MEDIA_ROOT/photos/

    def __str__(self):
        return self.title
