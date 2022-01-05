from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm
from .models import Person 
from django import forms

class PersonForm(ModelForm):
    class Meta:
        include = ('first_name', 'last_name')
        #exclude = ('votes', 'rating','tag', 'shares','pub_date')
        model = Person
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

