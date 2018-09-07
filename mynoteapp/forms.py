from django import forms
from django.contrib.auth.models import User
from mynoteapp.models import Note

from tinymce.widgets import TinyMCE

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=50, required=True, label='Логин')
	password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name', 'email')

class NoteForm(forms.ModelForm):
	#body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
	id = forms.CharField(max_length=25, label='ID',  required = False, widget=forms.HiddenInput())
	uuid = forms.CharField(max_length=25, label='Идентификатор', required = False)
	class Meta:
		model = Note
		fields = ('head', 'body', 'category', 'public', 'uuid')

	#если операция добавления (а не редактирования), то проверяем, чтобы uuid был уникальным в пределах пользователя
	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data['id'] == '' and cleaned_data['uuid'] != '':
			if len(Note.objects.filter(uuid=cleaned_data['uuid'], user=self.instance.user)) == 1:
				raise forms.ValidationError({'uuid':'Заметка стаким идентификатором уже существует'})
		return cleaned_data

class FilterForm(forms.ModelForm):
	create_date = forms.DateField(label='Дата создания',  required = False, widget=forms.TextInput(attrs={'placeholder': 'дд.мм.гггг'}))
	favorites = forms.ChoiceField(choices=((None, 'Без разницы'),(True, 'Да'),(False, 'Нет')), label='Избранная?',  required = False)
	class Meta:
		model = Note
		fields = ('head', 'category')
