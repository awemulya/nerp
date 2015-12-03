from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from training.forms import TrainingForm, CategoryForm, TargetGroupForm, ResourcePersonForm, ParticipantForm, \
    OrganizationForm
from training.models import Training, Category, ResourcePerson, TargetGroup, Participant, Organization, File
from training.serializers import ParticipantSerializer, OrganizationSerializer, FileSerializer
from users.models import group_required


def index(request):
    return render(request, 'training_index.html')


@group_required('Trainer')
def participants_as_json(request):
    items = Participant.objects.all()
    items_data = ParticipantSerializer(items, many=True).data
    return JsonResponse(items_data, safe=False)


@group_required('Trainer')
def print_training(request, pk):
    item = get_object_or_404(Training, pk=pk)
    return render(request, 'print_training.html', {'obj': item})


@group_required('Trainer')  # noqa
def training_form(request, pk=None):
    if pk:
        item = get_object_or_404(Training, pk=pk)
        scenario = 'Update'
    else:
        item = Training()
        scenario = 'Add'

    if request.POST:

        form = TrainingForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.starts == '':
                item.starts = None
            if item.ends == '':
                item.ends = None
            item.save()
            form.save_m2m()
            item.participants.clear()
            participants = request.POST.get('selected_participants').split(',')
            for participant in participants:
                if participant == u'':
                    continue
                participant_obj = Participant.objects.get(pk=participant)
                item.participants.add(participant_obj)
                # return redirect('/inventory/items/')
        descriptions = request.POST.getlist('descriptions')
        file_ids = request.POST.getlist('file_ids')
        if request.POST.get('deleted_files') == '':
            deleted_files = []
        else:
            deleted_files = request.POST.get('deleted_files').split(',')

        for index in request.POST.getlist('indices'):
            ind = int(index)
            file_id = file_ids[ind]
            if file_id == u'':
                the_file = File()
            else:
                the_file = File.objects.get(id=file_id)
            the_file.description = descriptions[ind]
            if request.FILES.get('files[' + index + ']'):
                the_file.file = request.FILES.get('files[' + index + ']')
            elif request.POST.get('clears[' + index + ']'):
                the_file.file = None
            the_file.training = item
            the_file.save()
        for deleted_file_id in deleted_files:
            # if deleted_file_id == '':
            # continue
            # try:
            the_file = File.objects.get(id=deleted_file_id)
            the_file.delete()
            # except File.DoesNotExist:
            # pass
        return redirect(reverse('update_training', kwargs={'pk': item.id}))

    else:
        form = TrainingForm(instance=item)
    if scenario == 'Update':
        participants = [x.id for x in item.participants.all()]
        training_files = item.files.all()
    else:
        participants = []
        training_files = []
    files = FileSerializer(training_files, many=True).data
    return render(request, 'training_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': 'training_base.html',
        'category_form': CategoryForm(instance=Category()),
        'resource_person_form': ResourcePersonForm(instance=ResourcePerson()),
        'target_group_form': TargetGroupForm(instance=TargetGroup()),
        'participant_form': ParticipantForm(instance=Participant()),
        'organization_form': OrganizationForm(instance=Organization()),
        'participants': participants,
        'files': files,
        'training_files': training_files,
    })


@group_required('Trainer')
def category_form(request, pk=None):
    if pk:
        item = get_object_or_404(Category, pk=pk)
        scenario = 'Update'
    else:
        item = Category()
        scenario = 'Create'
    if request.POST:
        form = CategoryForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            if request.is_ajax():
                return JsonResponse({'id': item.id, 'name': item.name})
            return redirect(reverse('list_categories'))
    else:
        form = CategoryForm(instance=item)
    return render(request, 'category_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': 'training_base.html',
    })


@group_required('Trainer')
def resource_person_form(request, pk=None):
    if pk:
        item = get_object_or_404(ResourcePerson, pk=pk)
        scenario = 'Update'
    else:
        item = ResourcePerson()
        scenario = 'Create'
    if request.POST:
        form = ResourcePersonForm(data=request.POST, instance=item)

        if form.is_valid():
            item = form.save()
            if request.is_ajax():
                return JsonResponse({'id': item.id, 'name': item.name})
            return redirect(reverse('list_resource_persons'))
        elif request.is_ajax():
            # TODO
            import ipdb

            ipdb.set_trace()
    else:
        form = ResourcePersonForm(instance=item)
    return render(request, 'resource_person_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': 'training_base.html',
    })


@group_required('Trainer')
def target_group_form(request, pk=None):
    if pk:
        item = get_object_or_404(TargetGroup, pk=pk)
        scenario = 'Update'
    else:
        item = TargetGroup()
        scenario = 'Create'
    if request.POST:
        form = TargetGroupForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            if request.is_ajax():
                return JsonResponse({'id': item.id, 'name': item.name})
            return redirect(reverse('list_target_groups'))
    else:
        form = TargetGroupForm(instance=item)
    return render(request, 'target_group_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': 'training_base.html',
    })


# @group_required('Trainer')
def participant_form(request, pk=None):
    if pk:
        item = get_object_or_404(Participant, pk=pk)
        scenario = 'Update'
    else:
        item = Participant()
        scenario = 'Create'
    if request.POST:
        form = ParticipantForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            if request.is_ajax():
                return JsonResponse(ParticipantSerializer(item).data, safe=False)
            return redirect(reverse('training_index'))
    else:
        form = ParticipantForm(instance=item)
    return render(request, 'participant_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': 'training_base.html',
    })


# @group_required('Trainer')
def organization_form(request, pk=None):
    if pk:
        item = get_object_or_404(Organization, pk=pk)
        scenario = 'Update'
    else:
        item = Organization()
        scenario = 'Create'
    if request.POST:
        form = OrganizationForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            if request.is_ajax():
                # return JsonResponse(OrganizationSerializer(item).data, safe=False)
                return render(request, 'callback.html', {'obj': OrganizationSerializer(item).data})
            return redirect(reverse('list_organizations'))
    else:
        form = OrganizationForm(instance=item)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'training_base.html'
    return render(request, 'organization_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@group_required('Trainer')
def list_trainings(request):
    items = Training.objects.all()
    return render(request, 'list_trainings.html', {'objects': items})


@group_required('Trainer')
def list_participants(request):
    items = Participant.objects.all()
    return render(request, 'list_participants.html', {'objects': items})


@group_required('Trainer')
def list_organizations(request):
    items = Organization.objects.all()
    return render(request, 'list_organizations.html', {'objects': items})


@group_required('Trainer')
def list_resource_persons(request):
    items = ResourcePerson.objects.all()
    return render(request, 'list_resource_persons.html', {'objects': items})


@group_required('Trainer')
def list_target_groups(request):
    items = TargetGroup.objects.all()
    return render(request, 'list_target_groups.html', {'objects': items})


@group_required('Trainer')
def list_categories(request):
    items = Category.objects.all()
    return render(request, 'list_categories.html', {'objects': items})


@group_required('Trainer')
def list_files(request):
    items = File.objects.all()
    return render(request, 'list_files.html', {'objects': items})


@group_required('Trainer')
def delete_training(request, pk):
    obj = get_object_or_404(Training, pk=pk)
    obj.delete()
    return redirect(reverse('list_trainings'))


@group_required('Trainer')
def delete_participant(request, pk):
    obj = get_object_or_404(Participant, pk=pk)
    obj.delete()
    return redirect(reverse('list_participants'))


@group_required('Trainer')
def delete_organization(request, pk):
    obj = get_object_or_404(Organization, pk=pk)
    obj.delete()
    return redirect(reverse('list_organizations'))


@group_required('Trainer')
def delete_category(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    obj.delete()
    return redirect(reverse('list_categories'))


@group_required('Trainer')
def delete_target_group(request, pk):
    obj = get_object_or_404(TargetGroup, pk=pk)
    obj.delete()
    return redirect(reverse('list_target_groups'))


@group_required('Trainer')
def delete_resource_person(request, pk):
    obj = get_object_or_404(ResourcePerson, pk=pk)
    obj.delete()
    return redirect(reverse('list_resource_persons'))


@group_required('Trainer')  # noqa
def training_report(request):
    items = Training.objects.all()
    if request.GET.get('from'):
        items = items.filter(starts__gte=request.GET.get('from'))
    if request.GET.get('to'):
        items = items.filter(starts__lte=request.GET.get('to'))
    resource_persons = []
    participants = []
    participations = 0
    days = 0
    total_resource_person_employments = 0
    for item in items:
        if item.starts and item.ends:
            days += item.days
        for participant in item.participants.all():
            participations += 1
            if participant not in participants:
                participants.append(participant)
        for resource_person in item.resource_persons.all():
            total_resource_person_employments += 1
            if resource_person not in resource_persons:
                resource_persons.append(resource_person)
    context = {
        'objects': items,
        'total_resource_person_employments': total_resource_person_employments,
        'total_resource_persons': len(resource_persons),
        'participants': len(participants),
        'participations': participations,
        'days': days,
    }
    return render(request, 'training_report.html', context)
