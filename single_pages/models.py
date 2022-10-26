import pwd
from django.db import models
from matplotlib.widgets import EllipseSelector
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    content = MarkdownxField()

    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1242/69e8e839d856a4f9/svg/{self.author.id}'