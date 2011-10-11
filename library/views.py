from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from library.forms import MediaForm
from library.models import Media, MediaType

@login_required
@require_POST
def row_count_preference(request):
    """
    Update the user's preference for the number of rows to show per page of
    the data grid.
    """
    request.session['row_count'] = request.POST.get('rows', 25)
    return HttpResponse()

@login_required
def media_list(request):
    """
    The main media listing page.
    """
    types = MediaType.objects.order_by('name')
    owners = User.objects.order_by('first_name')
    media = Media.objects
    type_filter = None
    owner_filter = None
    if request.method == 'POST':
        try:
            type_filter = MediaType.objects.get(pk=request.POST['type_filter'])
            request.session['type_filter'] = type_filter.id
        except:
            if 'type_filter' in request.session:
                del request.session['type_filter']
        try:
            owner_filter = User.objects.get(pk=request.POST['owner_filter'])
            request.session['owner_filter'] = owner_filter.id
        except:
            if 'owner_filter' in request.session:
                del request.session['owner_filter']
    else:
        if 'type_filter' in request.session:
            type_filter = MediaType.objects.get(pk=request.session.get('type_filter'))
        if 'owner_filter' in request.session:
            owner_filter = User.objects.get(pk=request.session.get('owner_filter'))
    context = {'types': types, 'owners': owners}
    if type_filter:
        media = media.filter(type=type_filter)
        context['type_filter'] = type_filter
    if owner_filter:
        media = media.filter(owners__id=owner_filter.id)
        context['owner_filter'] = owner_filter
    context['media_items'] = media.order_by('title')
    context['row_count'] = request.session.get('row_count', 25)
    return render_to_response('library/media_list.html', context,
                              context_instance=RequestContext(request))

class MediaCreateView(CreateView):
    model = Media
    form_class = MediaForm
    
    def form_valid(self, form):
        self.request.session['default_type'] = form.cleaned_data['type'].id
        self.request.session['default_owners'] = ','.join([str(owner.id) for owner in form.cleaned_data['owners']])
        return super(MediaCreateView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(MediaCreateView, self).get_form_kwargs()
        initial = kwargs['initial'] if kwargs.has_key('initial') else {}
        if 'default_type' in self.request.session:
            initial['type'] = MediaType.objects.get(pk=self.request.session['default_type'])
        if 'default_owners' in self.request.session:
            owner_ids = self.request.session['default_owners'].split(',')
            initial['owners'] = User.objects.filter(pk__in=owner_ids)
        kwargs['initial'] = initial
        return kwargs

    def get_success_url(self):
        if 'save_add' in self.request.POST:
            return reverse('media-add')
        else:
            return reverse('media-list')

class MediaDeleteView(DeleteView):
    model = Media

    def get_success_url(self):
        return reverse('media-list')

class MediaUpdateView(UpdateView):
    model = Media
    form_class = MediaForm

    def get_success_url(self):
        return reverse('media-list')
