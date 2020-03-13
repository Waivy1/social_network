from django.db import models


class User(models.Model):
    login = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, null=False)


class Post(models.Model):
    text = models.TextField(max_length=2000, null=False)


class LikedPosts(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_liked = models.BooleanField(null=False, default=True)

    def get_likes(self):
        return LikedPosts.objects.filter(post_id=self.post_id, is_liked=True).count()




