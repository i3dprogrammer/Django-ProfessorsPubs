from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, Http404
from django.views import View
from django.http import Http404
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Publication, ResearchField
from p_profile.models import ProfessorProfile

login_redirect_url = getattr(settings, 'LOGIN_URL', 'accounts:login')

class NewPublicationView(View):
    @method_decorator(login_required(login_url=login_redirect_url))
    def get(self, request, pub_id='-1'):
        if not ProfessorProfile.objects.filter(user=request.user).exists():
            return redirect('p_profile:create')

        context = {}
        if not pub_id == '-1':
            obj = get_object_or_404(Publication, id=pub_id)

            if not request.user == obj.user:
                raise Http404

            context = {
                'title': obj.title,
                'research_field': obj.research_field,
                'authors':obj.authors,
                'national':obj.national,
                'date':obj.date,
                'pub_type': obj.pub_type,
                'details': obj.details,
                'identifier': obj.identifier,
                'abstract': obj.abstract,
            }
        context['fields'] = ResearchField.objects.all()
        context['years'] = range(1980, timezone.now().year+1)
        return render(request, 'publications/create.html', context) #TODO

    @method_decorator(login_required(login_url=login_redirect_url))
    def post(self, request, pub_id='-1'):
        if not ProfessorProfile.objects.filter(user=request.user).exists():
            return redirect('p_profile:create')

        if not pub_id == '-1':
            pub = get_object_or_404(Publication, id=pub_id)
            if not request.user == pub.user:
                raise Http404

        errors = []
        try:
            title = request.POST.get('title')
            research_field = request.POST.get('research_field')
            authors = request.POST.get('authors')
            national = request.POST.get('national')
            date = request.POST.get('year')
            pub_type = request.POST.get('published_in')
            try:
                details = request.POST.getlist('details')[int(pub_type) - 1]
            except:
                details = ''
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
                'authors':authors,
                'national':national,
                'date':date,
                'published_in': pub_type,
                'details': details,
                'identifier': identifier,
                'abstract': abstract,
                'years': range(1980, timezone.now().year+1),
            }

            try:
                context['research_field'] = get_object_or_404(ResearchField, name=research_field)
            except:
                context['research_field'] = ''

            if title and research_field and authors and national and date and pub_type and details: # and identifier and abstract:

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
                    errors.append('Published in type cannot be empty.')
                if not details:
                    errors.append('Published in details cannot be empty.')
                # if not identifier:
                #     errors.append('Identifier field cannot be empty.')
                # if abstract == '':
                #     errors.append('Abstract field cannot be empty.')
                return render(request, 'publications/create.html', context) #TODO
        except:
            raise Http404

class PublicationView(View):
    @method_decorator(login_required(login_url=login_redirect_url))
    def get(self, request, pub_id):
        obj = get_object_or_404(Publication, id=pub_id)
        if not obj.user == request.user and not request.user.groups.filter(name='supervisor').exists():
            raise Http404()

        return render(request, 'publications/view_v2.html', {'publication': obj, 'can_change': obj.user == request.user})

class FilterView(View):
    @method_decorator(login_required(login_url=login_redirect_url))
    def get(self, request):
        if not request.user.groups.filter(name='supervisor').exists():
            raise Http404

        print_pub = request.GET.get('print', '')
        title = request.GET.get('title', '')
        authors = request.GET.get('authors', '')
        research_field = request.GET.get('research_field', '')
        nationality = request.GET.get('national', 'international')
        publication_year = request.GET.get('year')
        published_in = request.GET.getlist('published_in')
        journal_details = request.GET.get('journal_details', '')
        confrance_details = request.GET.get('confrance_details', '')
        book_details = request.GET.get('book_details', '')
        journal_id = request.GET.get('journal_identifier', '')
        book_id = request.GET.get('book_identifier', '')
        abstract = request.GET.get('abstract', '')

        pubs = Publication.objects.order_by('id')
        
        pubs = pubs.filter(title__contains=title)
        pubs = pubs.filter(authors__contains=authors)
        pubs = pubs.filter(research_field__name__contains=research_field)
        if publication_year:
            print('ye')
            pubs = pubs.filter(date=publication_year)
        pubs = pubs.filter(abstract__contains=abstract)
        if len(published_in) > 0:
            pubs = pubs.filter(pub_type__in=published_in)

        if nationality == 'International':
            pubs = pubs.filter(national=False)
        elif nationality == 'National':
            pubs = pubs.filter(national=True)

        filtered_pubs = []
        if 1 in published_in or '1' in published_in:
            filtered_pubs.extend(list(pubs.filter(pub_type='1', details__contains=journal_details, identifier__contains=journal_id)))
        if 2 in published_in or '2' in published_in:
            filtered_pubs.extend(list(pubs.filter(pub_type='2', details__contains=confrance_details)))
        if 3 in published_in or '3' in published_in:
            filtered_pubs.extend(list(pubs.filter(pub_type='3', details__contains=book_details, identifier__contains=book_id)))
        
        if len(filtered_pubs) == 0:
            filtered_pubs = pubs

        context = {
            'publications': filtered_pubs,
            'title': title,
            'authors': authors,
            'research_field': research_field,
            'nationality': nationality,
            'publication_year': publication_year,
            'published_in':published_in,
            'journal_details':journal_details,
            'confrance_details':confrance_details,
            'book_details':book_details,
            'journal_id':journal_id,
            'book_id':book_id,
            'abstract': abstract,
            'fields': ResearchField.objects.all(),
            'years': range(1980, timezone.now().year+1),
        }

        if print_pub == 'print':
            return render(request, 'publications/print.html', context)
        else:
            return render(request, 'publications/filter.html', context)