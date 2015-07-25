from django import forms
from django.core.urlresolvers import reverse_lazy
from models import Training, Category, TargetGroup, ResourcePerson, Participant, Organization
from app.utils.forms import KOModelForm, UserModelChoiceField

class TrainingForm(forms.ModelForm):
    #category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}), required=False)
    starts = forms.CharField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd', 'class': 'form-control'}), required=False)
    ends = forms.CharField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd', 'class': 'form-control'}), required=False)

    class Meta:
        model = Training
        exclude = ()


class CategoryForm(KOModelForm):
    class Meta:
        model = Category
        exclude = ()


class ResourcePersonForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    organization = forms.ModelChoiceField(Organization.objects.all(), widget=forms.Select(
        attrs={'class': 'selectize', 'data-url': reverse_lazy('add_organization')}), required=False)

    class Meta:
        model = ResourcePerson
        exclude = ()


class TargetGroupForm(KOModelForm):
    class Meta:
        model = TargetGroup
        exclude = ()


class ParticipantForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    organization = forms.ModelChoiceField(Organization.objects.all(), widget=forms.Select(
        attrs={'class': 'selectize', 'data-url': reverse_lazy('add_organization')}), required=False)

    class Meta:
        model = Participant
        exclude = ()


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ()