from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import Http404
from django.utils.decorators import method_decorator

from django.utils import timezone

from .models import Publication, ResearchField

login_redirect_url = getattr(settings, 'LOGIN_URL', 'accounts:login')

class NewPublicationView(View):
    @method_decorator(login_required(login_url=login_redirect_url))
    def get(self, request, pub_id='-1'):
        context = {
            'fields': ResearchField.objects.all(),
			'years': range(1980, timezone.now().year+1),
        }
        if not pub_id == '-1':
            obj = get_object_or_404(Publication, id=pub_id)
            context = {
                'fields': ResearchField.objects.all(),
                'title': obj.title,
                'research_field': obj.research_field,
                'authors':obj.authors,
                'national':obj.national,
                'date':obj.date,
                'pub_type': obj.pub_type,
                'details': obj.details,
                'identifier': obj.identifier,
                'abstract': obj.abstract,
                'years': range(1980, timezone.now().year+1),
            }
        return render(request, 'publications/create.html', context) #TODO

    @method_decorator(login_required(login_url=login_redirect_url))
    def post(self, request, pub_id='-1'):
        errors = []

        title = request.POST.get('title')
        research_field = request.POST.get('research_field')
        authors = request.POST.get('authors')
        national = request.POST.get('national')
        date = request.POST.get('year')
        pub_type = request.POST.get('published_in')
        details = request.POST.getlist('details')[int(pub_type) - 1]
        identifier = request.POST.getlist('identifier')
        abstract = request.POST.get('abstract')

        if pub_type == '1':
            identifier = identifier[0]
        elif pub_type == '3':
            identifier = identifier[1]
        else:
            identifier = 'None'

        context = {
            'errors': errors,
            'fields': ResearchField.objects.all(),
            'title': title,
            'research_field': get_object_or_404(ResearchField, name=research_field),
            'authors':authors,
            'national':national,
            'date':date,
            'published_in': pub_type,
            'details': details,
            'identifier': identifier,
            'abstract': abstract,
            'years': range(1980, timezone.now().year+1),
        }

        if title and research_field and authors and national and date and pub_type and details and identifier and abstract:

            if not pub_id=='-1':
                obj = get_object_or_404(Publication, id=pub_id)
            else:
                obj = Publication()
            obj.user = request.user
            obj.title = title
            obj.research_field = get_object_or_404(ResearchField, name=research_field)
            obj.authors = authors
            obj.national = (national == "National")
            obj.date = date
            obj.pub_type = pub_type
            obj.details = details
            obj.identifier = identifier
            obj.abstract = abstract
            obj.save()

            return redirect('publications:view', pub_id = obj.id) #TODO
        else:
            if title == '':
                errors.append('Title field cannot be empty.')
            if research_field == '':
                errors.append('Research field cannot be empty.')
            if authors == '':
                errors.append('Authors field cannot be empty.')
            if national == '':
                errors.append('National/International field cannot be empty.')
            if date == '':
                errors.append('Publication year cannot be empty.')
            if pub_type == None:
                errors.append('Published in field cannot be empty.')
            if not details:
                errors.append('Details/Name field cannot be empty.')
            if not identifier:
                errors.append('Identifier field cannot be empty.')
            if abstract == '':
                errors.append('Abstract field cannot be empty.')
            print(errors)
            return render(request, 'publications/create.html', context) #TODO

class PublicationView(View):
    @method_decorator(login_required(login_url=login_redirect_url))
    def get(self, request, pub_id):
        obj = get_object_or_404(Publication, id=pub_id)
        if not obj.user == request.user and not request.user.groups.filter(name='supervisor').exists():
            raise Http404()

        return render(request, 'publications/view_v2.html', {'publication': obj})