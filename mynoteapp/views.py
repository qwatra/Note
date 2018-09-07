from django.shortcuts import render, redirect
from mynoteapp.forms import UserForm, NoteForm, FilterForm
from mynoteapp.models import Note

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict
import json
import re

from django.http import Http404

# Create your views here.
@login_required(login_url='login/')
def home(request):
	edit_form = NoteForm()
	filter_form = FilterForm()
	notes = []
	for note in Note.objects.filter(user=request.user).order_by('-create_date'):
		body = re.sub('<[^>]*>', '', str(note.body))
		notes.append({
			'id': 'n'+str(note.id),
			'head': note.head if len(note.head)<15 else note.head[:12]+'...',
			'body': body if len(body)<120 else body[:120]+'...',
			'favorite': 'favorite' if note.favorites else ''
			})
	return render(request, 'mynote/home.html', {'notes':notes, 'edit_form':edit_form, 'filter_form':filter_form})

def reg(request):
	user_form = UserForm()

	if request.method=='POST':
		user_form = UserForm(request.POST)
		if user_form.is_valid():
			User.objects.create_user(**user_form.cleaned_data)

			login(request, authenticate(
					username=user_form.cleaned_data['username'],
					password=user_form.cleaned_data['password']))
			return redirect(home)

	return render(request, 'registration/registration.html', {'form': user_form})

def get_public_note(request, user_login, uuid):
	try:
		user = User.objects.get(username=user_login)
		note = Note.objects.get(user=user, uuid=uuid, public = True)
		return render(request, 'mynote/note.html', {'title':note.head, 'body': str(note.body)})
	except Exception:
		raise Http404("Poll does not exist")

def ajax_hendler(request):
	if request.method == 'GET':
		try:
			if request.GET.get('action') == 'getsortednotes':
				field = request.GET.get('field')
				if request.GET.get('orderby') == 'desc':
					field = '-'+field
				notes = []
				for note in Note.objects.filter(user=request.user).order_by(field):
					body = re.sub('<[^>]*>', '', str(note.body))
					notes.append({
						'id': 'n'+str(note.id),
						'head': note.head if len(note.head)<15 else note.head[:12]+'...',
						'body': body if len(body)<120 else body[:120]+'...',
						'favorite': 'favorite' if note.favorites else ''
						})
				return JsonResponse({'success':True, 'notes':notes})

			if request.GET.get('action') == 'getfilterednotes':
				form = FilterForm(request.GET)
				if form.is_valid():
					if form.cleaned_data['head']=='':
						del(form.cleaned_data['head'])
					if form.cleaned_data['create_date'] is None:
						del(form.cleaned_data['create_date'])
					else:
						d = form.cleaned_data['create_date']
						del(form.cleaned_data['create_date'])
						form.cleaned_data['create_date__date'] = d
					if form.cleaned_data['category'] is None:
						del(form.cleaned_data['category'])
					if form.cleaned_data['favorites'] == '':
						del(form.cleaned_data['favorites'])
					form.cleaned_data['user'] = request.user

					notes = []
					for note in Note.objects.filter(**form.cleaned_data):
						body = re.sub('<[^>]*>', '', str(note.body))
						notes.append({
							'id': 'n'+str(note.id),
							'head': note.head if len(note.head)<15 else note.head[:12]+'...',
							'body': body if len(body)<120 else body[:120]+'...',
							'favorite': 'favorite' if note.favorites else ''
							})
					return JsonResponse({'success':True, 'notes':notes})
				else:
					response = {'success':False,
						'errors': dict([(k, [e for e in v]) for k, v in form.errors.items()])}
					return JsonResponse(response)


			id = request.GET.get('id')[1:]
			n = Note.objects.get(id=id, user=request.user)
			if request.GET.get('action') == 'get':
				d = model_to_dict(n)
				if n.category is not None:
					d['category'] = n.category.id
				return JsonResponse(model_to_dict(n))

			elif request.GET.get('action') == 'del':
				n.delete()
				return JsonResponse({'succses':True,
					'id': 'n'+id})

			elif request.GET.get('action') == 'set_favorite':
				n.favorites = request.GET.get('value') == 'true'
				n.save()
				return JsonResponse({'succses':True,
					'id': 'n'+id,
					'value': n.favorites})
		except Exception:
			return HttpResponseBadRequest("Такой заметки не существует")

	#Создаем/обновляем заметку
	if request.method =='POST':
		if request.POST.get('id') == '': #создаем заметку
			note_form = NoteForm(request.POST)
			note_form.instance.user_id = request.user.id
		else: # получаем заметку из бд
			n = Note.objects.get(id=request.POST.get('id'), user=request.user)
			note_form = NoteForm(request.POST, instance=n)

		if note_form.is_valid():
			if request.POST.get('id') == '':
				note = note_form.save(commit=False)
				note.user = request.user
				note.save();
			else:
				note = note_form.save()
			body = re.sub('<[^>]*>', '', str(note.body))
			return JsonResponse({'succses':True,
				'note':{
					'id': 'n'+str(note.id),
					'head': note.head if len(note.head)<15 else note.head[:12]+'...',
					'body': body if len(body)<120 else body[:120]+'...',
					'favorite': ' favorite' if note.favorites else ''
					}})
		else: 
			response = {'succses':False,
				'errors': dict([(k, [e for e in v]) for k, v in note_form.errors.items()])}
			return JsonResponse(response)