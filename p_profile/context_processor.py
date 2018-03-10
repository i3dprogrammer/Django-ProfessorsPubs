def supervisor_processor(request):
    supervisor = False
    if request.user.groups.filter(name='supervisor').exists():
        supervisor = True
    return {'supervisor': supervisor }