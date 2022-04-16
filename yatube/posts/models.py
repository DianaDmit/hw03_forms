from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group (models.Model):
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL',)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа'
    )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name='Статья',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Комментарий',
    )
    created = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True
    )

    def __str__(self):
        return self.text
