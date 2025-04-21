from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import Permission,  AbstractUser, Group, User
class Category(models.Model):
    """категори"""

    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описания")
    url = models.SlugField(max_length=160, unique=True)

    def str(self):
        return self.name

class Actor(models.Model):
    """Актери и режусерии"""

    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описания")
    image = models.ImageField("Изаброжение", upload_to="actors/")

    def str(self):
        return self.name

    class Meta:
        verbose_name = "Актери и режусерии"
        verbose_name_plural = "Актери и режусерии"

class Genre(models.Model):
    """Жанры"""

    name = models.CharField("имя", max_length=100)
    description = models.TextField("Описания")
    url = models.SlugField(max_length=160, unique=True)

    def str(self):
        return self.name

    class Meta:
        verbose_name = "Жанры"
        verbose_name_plural = "Жанры"

class Movie(models.Model):
    """филмь"""

    title = models.CharField("Названия", max_length=100)
    tagline = models.CharField("слоган", max_length=100, default='')
    description = models.TextField("Описания")
    poster = models.ImageField("постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("дата выхода", default=2019)
    country = models.CharField("страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режжиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="Актери", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    world_premier = models.DateField("примера в мире", default=date.today)
    budget = models.PositiveSmallIntegerField("бюджет", default=0, help_text="указывать сумму в доларах")
    fees_in_use = models.PositiveSmallIntegerField("сборы в сша", default=0, help_text="указывать сумму в доларах")
    fees_in_world = models.PositiveSmallIntegerField("сборы в мире", default=0, help_text="указывать сумму в доларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("чорнавик", default=False)
    def str(self):
        return self.title

    class Meta:
        verbose_name = "филмь"
        verbose_name_plural = "филмь"

class MovieShots(models.Model):
    """кадры из фильма"""

    title = models.CharField("заголовок", max_length=100)
    description = models.TextField("Описания")
    image = models.ImageField("Изаброжение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def str(self):
        return self.title

    class Meta:
        verbose_name = "кадры из фильма"
        verbose_name_plural = "кадры из фильма"

class RetigStar(models.Model):
    """звезда рейтинка"""

    value = models.PositiveSmallIntegerField("значение", default=0)

    def str(self):
        return self.value

    class Meta:
        verbose_name = "звезда рейтинка"
        verbose_name_plural = "звезда рейтинка"

class Reting(models.Model):
    """рейтинг"""

    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RetigStar, on_delete=models.CASCADE, verbose_name="звезта")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")

    def str(self):
        return f"{self.star}-{ self.movie}"

    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинг"

class Reviews(models.Model):
    """отзывы"""
    email = models.EmailField()
    name = models.CharField("имя", max_length=100)
    text = models.TextField("собшения", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Радитель", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def str(self):
        return f"{self.name}-{self.movie}"

    class Meta:
        verbose_name = "отзывы"
        verbose_name_plural = "отзыв"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    number = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class UserCustom(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
