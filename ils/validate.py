from django.db import models
from django.utils.six import with_metaclass
import re, time
from django.core import exceptions

class CustomField(with_metaclass(models.SubfieldBase, models.Field)):
# class CustomField(models.Field):

	description = "Custom date field"

	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 250
		super(CustomField, self).__init__(self, *args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super(CustomField, self).deconstruct()
		if kwargs['verbose_name']:
			del kwargs['verbose_name']
		del kwargs['max_length']
		return name, path, args, kwargs

	def get_db_prep_value(self, value, connection, prepared=False):
		date = re.compile('^[0-2]\d{3}([-])(0[1-9]|1[012]|[1-9])([-])(0[1-9]|[12][0-9]|3[01]|[0-9])$')
		date_year = re.compile('^[0-2]\d{3}$')
		date_year_month = re.compile('^[0-2]\d{3}([-])(0[1-9]|1[012]|[1-9])$')

		if date.match(value):
			try:
				timestamp = time.strptime(value, '%Y-%m-%d')
				value = '{0}-{1}-{2:02}'.format(timestamp.tm_year, timestamp.tm_mon, timestamp.tm_mday % 100)
				return value
			except:
				error_str = "Invalid Date"
				raise Exception('%s' % error_str)
				# raise exceptions.ValdationError("Date not in format YYYY-MM-DD")
		elif date_year_month.match(value):
			try:
				timestamp = time.strptime(value, '%Y-%m')
				value = '{0}-{1}'.format(timestamp.tm_year, timestamp.tm_mon % 100)
				return value
			except ValueError:
				return "Date not in format YYYY-MM"
		elif date_year.match(value):
			try:
				timestamp = time.strptime(value, '%Y')
				return timestamp.tm_year
			except ValueError:
				return "Date not in format YYYY"
		else:
			raise ValueError("Please Insert valid date")
		

	def to_python(self, value):
		return value

	def get_internal_type(self):
		return "CharField"

	def formfield(self, **kwargs):
		defaults = {'form_class': CustomField}
		defaults.update(kwargs)
		return super(CustomField, self).formfield(**defaults)
