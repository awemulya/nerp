from django.db import models
from django.utils.six import with_metaclass
import re, time
from django import forms

class FlexibleDateFormField(forms.Field):
	def __init__(self, *args, **kwargs):
		super(FlexibleDateFormField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		date = re.compile('^[0-2]\d{3}([-])(0[1-9]|1[012]|[1-9])([-])(0[1-9]|[12][0-9]|3[01]|[0-9])$')
		date_year = re.compile('^[0-2]\d{3}$')
		date_year_month = re.compile('^[0-2]\d{3}([-])(0[1-9]|1[012]|[1-9])$')

		if date.match(value):
			try:
				timestamp = time.strptime(value, '%Y-%m-%d')
				value = '{0}-{1}-{2:02}'.format(timestamp.tm_year, timestamp.tm_mon, timestamp.tm_mday % 100)
				return value
			except ValueError, e:
				raise forms.ValidationError("%s" % e)
		elif date_year_month.match(value):
			try:
				timestamp = time.strptime(value, '%Y-%m')
				value = '{0}-{1}'.format(timestamp.tm_year, timestamp.tm_mon % 100)
				return value
			except ValueError, e:
				raise forms.ValidationError("%s" % e)
		elif date_year.match(value):
			try:
				timestamp = time.strptime(value, '%Y')
				return timestamp.tm_year
			except ValueError, e:
				raise forms.ValidationError("%s" % e)
		else:
			raise forms.ValidationError("Invalid Date Format")

class FlexibleDateField(with_metaclass(models.SubfieldBase, models.Field)):

	description = "Flexible date field"

	def to_python(self, value):
		if value == None:
			return None
		return value

	def get_internal_type(self):
		return "CharField"

	def formfield(self, **kwargs):
		defaults = {'form_class': FlexibleDateFormField}
		defaults.update(kwargs)
		return super(FlexibleDateField, self).formfield(**defaults)
