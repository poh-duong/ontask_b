# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import pytz

from django.conf import settings as ontask_settings
import django_tables2 as tables
from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect, reverse, render
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_tables2 import A
from django.db.models import Q

from ontask.permissions import is_instructor
from workflow.ops import get_workflow
from .models import Log
from .ops import log_types


class LogTable(tables.Table):
    # Needs to be in the table to be used as URL parameter
    id = tables.Column(visible=False)

    created = tables.DateTimeColumn(
        attrs={'td': {'class': 'dt-body-center'}},
        orderable=False,
        verbose_name='Date/Time',
        format=str('r'),
        short=True)

    user = tables.EmailColumn(
        attrs={'td': {'class': 'dt-body-center'}},
        orderable=False,
        accessor=A('user.email')
    )

    name = tables.Column(
        attrs={'td': {'class': 'dt-body-center'}},
        orderable=False,
        verbose_name=str('Event type')
    )

    operations = tables.Column(
        empty_values=[],
        attrs={'td': {'class': 'dt-body-center'}},
        orderable=False,
        verbose_name=str('Additional data')
    )

    def __init__(self, data, *args, **kwargs):
        super(LogTable, self).__init__(data, *args, **kwargs)

    def render_operations(self, record):
        return format_html(
            """
            <button type="submit" class="btn btn-primary btn-sm js-log-view"
                    data-url="{0}">
              <span class="glyphicon glyphicon-eye-open"></span> View
            </button>
            """.format(reverse('logs:view', kwargs={'pk': record.id}))
        )

    class Meta:
        model = Log

        fields = ('created', 'user', 'name', 'operations')

        sequence = ('created', 'user', 'name', 'operations')

        exclude = ('id', 'workflow', 'payload')

        attrs = {
            'class': 'table display',
            'id': 'log-table'
        }


@user_passes_test(is_instructor)
def show(request):
    # Try to get workflow and if not present, go to home page
    workflow = get_workflow(request)
    if not workflow:
        return redirect('workflow:index')

    # Create the context with the column names
    context = {
        'workflow': workflow,
        'column_names': ['Date/Time', 'User', 'Event type', 'View']
    }

    # Render the page with the table
    return render(request, 'logs/show.html', context)


@user_passes_test(is_instructor)
@csrf_exempt
@require_http_methods(['POST'])
def show_ss(request):
    # Try to get workflow and if not present, go to home page
    workflow = get_workflow(request)
    if not workflow:
        return JsonResponse({'error': 'Incorrect request. Unable to process'})

    # Check that the GET parameter are correctly given
    try:
        draw = int(request.POST.get('draw', None))
        start = int(request.POST.get('start', None))
        length = int(request.POST.get('length', None))
    except ValueError:
        return JsonResponse({'error': 'Incorrect request. Unable to process'})

    # Get the column information from the request and the rest of values.
    search_value = request.POST.get('search[value]', None)

    # Get the logs
    if search_value:
        qs = Log.objects.filter(
            Q(user__email__contains=search_value) |
            Q(name__contains=search_value),
            workflow__id=workflow.id,
        ).distinct().order_by(F('created').desc()).values_list(
            'id', 'created', 'user__email', 'name')
    else:
        qs = Log.objects.filter(
            workflow__id=workflow.id
        ).order_by(F('created').desc()).values_list(
            'id', 'created', 'user__email', 'name')

    final_qs = []
    for item in qs[start:start + length]:
        row = [
            item[1].astimezone(pytz.timezone(ontask_settings.TIME_ZONE)),
            item[2],
            item[3],
            """
            <button type="submit" class="btn btn-primary btn-sm js-log-view"
                    data-url="{0}">
              <span class="glyphicon glyphicon-eye-open"></span> View
            </button>
            """.format(reverse('logs:view', kwargs={'pk': item[0]}))]

        # Add the row to the final query_set
        final_qs.append(row)

    # Result to return as AJAX response
    data = {
        'draw': draw,
        'recordsTotal': Log.objects.all().count(),
        'recordsFiltered': len(qs),
        'data': final_qs
    }
    # Render the page with the table
    return JsonResponse(data)


@user_passes_test(is_instructor)
def view_log_list(request, pk):
    # Get the log item
    log_item = Log.objects.get(pk=pk)
    data = dict()

    context = log_item.get_payload()

    # Add the name of the object, the workflow and the type
    context['log_type'] = log_item.name
    context['op_name'] = log_types[log_item.name]
    context['workflow'] = log_item.workflow

    # Render the template and return as JSON response
    data['html_form'] = render_to_string(
        'logs/includes/partial_log_view.html',
        context,
        request=request)

    return JsonResponse(data)