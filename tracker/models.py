from django.db import models
from django.contrib.auth.models import User

# ✅ 1. UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    eco_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

# ✅ 2. Goal Model (defined early so others can reference it)
CATEGORY_CHOICES = [
    ('waste', 'Waste Reduction'),
    ('energy', 'Energy Saving'),
    ('transport', 'Green Transportation'),
    ('food', 'Sustainable Food'),
]

class Goal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_goals', blank=True)

    def __str__(self):
        return self.title

# ✅ 3. Like Model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'goal')

# ✅ 4. Comment Model
class Comment(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()  # make sure this is `text`, not `content`
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.goal.title}'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')  # <-- Add related_name
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

