from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=256, verbose_name='Название')

	class Meta:
		verbose_name='Категория'
		verbose_name_plural='Категории'
		ordering=['name']

	def __str__(self):
		return self.name

class Note(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	head = models.CharField(max_length=50, verbose_name='Заголовок', blank=True)
	#body = models.TextField(verbose_name='Текст заметки')
	body = tinymce_models.HTMLField('Текст заметки')
	create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория', blank=True)
	favorites = models.BooleanField(default=False, verbose_name='Избранная')
	uuid = models.CharField(max_length=25, blank=True, verbose_name='Идентификатор')
	public =  models.BooleanField(default=False, verbose_name='Публичная заметка')

	class Meta:
		verbose_name='Заметка'
		verbose_name_plural='Заметки'

	def __str__(self):
		return self.head if self.head else self.body[:25]