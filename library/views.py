"""
View functions for the library application.

.. module:: library.views
   :synopsis: View functions for the library application

.. moduleauthor:: Jeremy Bowman <jmbowman@alum.mit.edu>

"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import django.utils.simplejson as json
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from library.forms import MediaForm
from library.models import Media, MediaType


@login_required
@require_POST
def row_count_preference(request):
    """Update the user's rows per page preference for the data grid."""
    request.session['row_count'] = request.POST.get('rows', 25)
    return HttpResponse()


@login_required
def media_list(request):
    """The main media listing page."""
    types = MediaType.objects.order_by('name')
    owners = User.objects.order_by('first_name')
    session = request.session
    type_filter = None
    owner_filter = None
    if request.method == 'POST':
        try:
            type_filter = MediaType.objects.get(pk=request.POST['type_filter'])
            session['type_filter'] = type_filter.id
        except:
            if 'type_filter' in session:
                del session['type_filter']
        try:
            owner_filter = User.objects.get(pk=request.POST['owner_filter'])
            session['owner_filter'] = owner_filter.id
        except:
            if 'owner_filter' in session:
                del session['owner_filter']
    else:
        if 'type_filter' in session:
            type_filter = MediaType.objects.get(pk=session.get('type_filter'))
        if 'owner_filter' in session:
            owner_filter = User.objects.get(pk=session.get('owner_filter'))
    context = {'types': types, 'owners': owners}
    if type_filter:
        context['type_filter'] = type_filter
    if owner_filter:
        context['owner_filter'] = owner_filter
    context['row_count'] = session.get('row_count', 25)
    return render_to_response('library/media_list.html', context,
                              context_instance=RequestContext(request))


@login_required
def grid_data(request):
    """Handle requests from the DataTables widget for data to display."""
    get = request.GET
    media = Media.objects
    session = request.session

    # selected filters
    if 'type_filter' in session:
        media = media.filter(type__id=session.get('type_filter'))
    if 'owner_filter' in session:
        media = media.filter(owners__id=session.get('owner_filter'))

    # search box
    if 'sSearch' in get:
        term = get['sSearch']
        if term:
            media = media.filter(Q(title__icontains=term) |
                                 Q(type__name__icontains=term) |
                                 Q(owners__first_name__icontains=term))
            media = media.distinct()
    filtered = media

    # sorting
    columns = ['title', 'type__name']
    sort_count = max(int(get.get('iSortingCols', 0)), 0)
    sort_cols = []
    for i in range(sort_count):
        key = 'iSortCol_{0}'.format(i)
        if not key in get:
            break
        entry = columns[int(get[key])]
        if get.get('sSortDir_{0}'.format(i), 'asc') == 'desc':
            entry = '-' + entry
        sort_cols.append(entry)
    if sort_cols:
        media = media.order_by(*sort_cols)

    # paging
    if 'iDisplayStart' in get and 'iDisplayLength' in get:
        start = max(int(get['iDisplayStart']), 0)
        end = start + min(int(get['iDisplayLength']), 100)
        media = media[start:end]

    media = media.prefetch_related('owners', 'type')
    aaData = [['<a href="{0}">{1}</a>'.format(reverse('media-edit',
                                                      args=[item.id]),
                                              item.title),
               item.type.name,
               ', '.join([u.first_name for u in item.sorted_owners()])] \
              for item in media]
    context = {
        'aaData': aaData,
        'iTotalDisplayRecords': filtered.count(),
        'iTotalRecords': Media.objects.count(),
        'sEcho': int(get.get('sEcho', 0)),
    }
    return HttpResponse(json.dumps(context))


class MediaCreateView(CreateView):

    """View for creating new media items."""

    model = Media
    form_class = MediaForm

    def form_valid(self, form):
        """Process a valid submitted instance of the form.

        Overridden to store the media type and owners list in the session for
        use as the defaults for subsequently created items.

        """
        self.request.session['default_type'] = form.cleaned_data['type'].id
        owner_ids = [str(owner.id) for owner in form.cleaned_data['owners']]
        self.request.session['default_owners'] = ','.join(owner_ids)
        return super(MediaCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        """Build the keyword arguments required to instantiate the form.

        Overridden to use the default type and owners from the session, if any.

        """
        kwargs = super(MediaCreateView, self).get_form_kwargs()
        initial = kwargs['initial'] if 'initial' in kwargs else {}
        session = self.request.session
        if 'default_type' in session:
            initial['type'] = MediaType.objects.get(pk=session['default_type'])
        if 'default_owners' in session:
            owner_ids = session['default_owners'].split(',')
            initial['owners'] = User.objects.filter(pk__in=owner_ids)
        kwargs['initial'] = initial
        return kwargs

    def get_success_url(self):
        """Get the appropriate URL to redirect to on successful submission.

        Supports "Save and Add Another" by redirecting the user to a fresh
        instance of the form when appropriate.

        """
        if 'save_add' in self.request.POST:
            return reverse('media-add')
        else:
            return reverse('media-list')


class MediaDeleteView(DeleteView):

    """Media item deletion view."""

    model = Media

    def get_success_url(self):
        """Specify the media listing as the post-deletion destination URL."""
        return reverse('media-list')


class MediaUpdateView(UpdateView):

    """View for editing existing media items."""

    model = Media
    form_class = MediaForm

    def get_success_url(self):
        """Specify the media listing as the post-edit destination URL."""
        return reverse('media-list')
