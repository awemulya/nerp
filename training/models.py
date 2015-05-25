import os
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from froala_editor.fields import FroalaField


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class TargetGroup(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone_no = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(blank=True, null=True, max_length=50)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_no = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class ResourcePerson(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_no = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Training(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    # starts = models.DateTimeField(blank=True, null=True)
    # ends = models.DateTimeField(blank=True, null=True)
    starts = models.DateField(blank=True, null=True)
    ends = models.DateField(blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='trainings', blank=True)
    target_groups = models.ManyToManyField(TargetGroup, related_name='trainings', blank=True)
    criteria_for_selection = FroalaField(blank=True, null=True)
    objective = FroalaField(blank=True, null=True)
    output = FroalaField(blank=True, null=True)
    conclusion = FroalaField(blank=True, null=True)
    feedback = FroalaField(blank=True, null=True)
    curriculum = FroalaField(blank=True, null=True)
    resource_persons = models.ManyToManyField(ResourcePerson, related_name='trainings', blank=True)
    participants = models.ManyToManyField(Participant, related_name='trainings', blank=True)

    @property
    def days(self):
        delta = self.ends - self.starts
        return delta.days + 1

    @property
    def resource_persons_count(self):
        return self.resource_persons.count()

    @property
    def participants_count(self):
        return self.resource_persons.count()

    def __str__(self):
        return self.title


class File(models.Model):
    description = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to='training/files/')
    training = models.ForeignKey(Training, related_name='files')

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.description