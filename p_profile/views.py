from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Affiliation, Department, ProfessorProfile
from publications.models import Publication

login_redirect_url = getattr(settings, 'LOGIN_URL', 'accounts:login')


class CreateProfessorProfileView(View):
    @method_decorator(login_required(login_url=login_redirect_url))
    def get(self, request, edit=False):
        if ProfessorProfile.objects.filter(user=request.user).exists():
            return redirect('p_profile:view')
        
        context = {
            'affiliations': Affiliation.objects.all(),
            'departments': Department.objects.all(),
        }
        if edit == True:
            obj = get_object_or_404(ProfessorProfile, user=request.user)
            context = {
                'affiliations': Affiliation.objects.all(),
                'departments': Department.objects.all(),
                'name': obj.name,
                'speciality': obj.speciality,
                'department': obj.department,
                'affiliation': obj.affiliation,
            }

        return render(request, 'pprofile/create.html', context) #TODO

    @method_decorator(login_required(login_url=login_redirect_url))
    def post(self, request):
        errors = []
        name = request.POST.get('name')
        speciality = request.POST.get('speciality')
        department = request.POST.get('department')
        affiliation = request.POST.get('affiliation')

        context = {
            'affiliations': Affiliation.objects.all(),
            'departments': Department.objects.all(),
            'name': name,
            'speciality': speciality,
            'department': department,
            'affiliation': affiliation,
            'errors': errors,
        }

        if name and speciality and department and affiliation:
            if ProfessorProfile.objects.filter(user=request.user).exists():
                obj = ProfessorProfile.objects.get(user=request.user)
            else:
                obj = ProfessorProfile()
            obj.user = request.user
            obj.name = name
            obj.speciality = speciality
            obj.department = get_object_or_404(Department, name=department)
            obj.affiliation = get_object_or_404(Affiliation, name=affiliation)
            obj.save()
            return redirect('p_profile:view')
        else:
            if name == '':
                errors.append('Name field cannot be empty!')
            if speciality == '':
                errors.append('Speciality field cannot be empty!')
            if department == '':
                errors.append('Department field cannot be empty!')
            if affiliation == '':
                errors.append('Affiliation field cannot be empty!')
            return render(request, 'pprofile/create.html', context) # TODO


class ProfessorProfileView(View):
    @method_decorator(login_required(login_url=login_redirect_url))
    def get(self, request):
        if not ProfessorProfile.objects.filter(user=request.user).exists():
            return redirect('p_profile:create')
        
        

        if request.user.groups.filter(name='supervisor').exists():
            paginator = Paginator(Publication.objects.order_by('-id'), 10)
        else:
            paginator = Paginator(Publication.objects.filter(user=request.user).order_by('-id'), 10)

        page = request.GET.get('page')

        try:
            publications = paginator.page(page)
        except PageNotAnInteger:
            publications = paginator.page(1)
        except EmptyPage:
            publications = paginator.page(paginator.num_pages)

        context = {
            'profile': get_object_or_404(ProfessorProfile, user=request.user),
            'publications': publications,
        }



        return render(request, 'pprofile/view_2.html', context)
