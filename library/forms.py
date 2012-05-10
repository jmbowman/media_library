"""
Form definitions for the library application.

.. module:: library.forms
   :synopsis: Form definitions for the library application

.. moduleauthor:: Jeremy Bowman <jmbowman@alum.mit.edu>

"""

from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from uni_form.helpers import Button, FormHelper, Submit

from library.models import Media


class StyledForm(forms.ModelForm):

    """Base class for all our forms.

    Has Django automatically style the input fields based on state.

    """

    error_css_class = 'error'
    required_css_class = 'required'


class MediaForm(StyledForm):

    """Media item entry form."""

    owners = forms.ModelMultipleChoiceField(User.objects,
        widget=forms.SelectMultiple(attrs={'size': '6'}))

    @property
    def helper(self):
        """django-uni-form layout specification."""
        helper = FormHelper()
        if self.instance and self.instance.id:
            helper.form_action = reverse('media-edit', args=[self.instance.id])
            delete = Button('delete', 'Delete This Item',
                            css_class='secondaryAction')
            helper.add_input(delete)
        else:
            helper.form_action = reverse('media-add')
            another = Submit('save_add', 'Save and Add Another',
                             css_class='primaryAction')
            helper.add_input(another)
        submit = Submit('save', 'Save', css_class='primaryAction')
        helper.add_input(submit)
        helper.form_method = 'POST'
        return helper

    class Meta:
        model = Media
