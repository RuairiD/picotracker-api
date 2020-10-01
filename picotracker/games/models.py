from django.db import models


class Developer(models.Model):
    username = models.CharField(max_length=255)
    bbs_id = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.username}'
    class Meta:
        verbose_name = 'Developer'
        verbose_name_plural = 'Developers'


class Game(models.Model):
    name = models.CharField(max_length=255)
    bbs_id = models.PositiveIntegerField()
    stars = models.PositiveIntegerField()
    comments = models.PositiveIntegerField()
    rating = models.FloatField(default=0)
    image_url = models.URLField()

    time_created = models.DateTimeField()
    developer = models.ForeignKey(
        Developer,
        related_name='games',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} by {self.developer.username}'

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
