from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', ListTasksView.as_view(), name='list_tasks'),
    url(r'^incomplete/$',
        ListIncompleteTasksView.as_view(),
        name='list_incomplete_tasks'),
    url(r'^standby/$',
        ListStandByTasksView.as_view(),
        name='list_standby_tasks'),
    url(r'^completed/$',
        ListCompletedTasksView.as_view(),
        name='list_completed_tasks'),
    url(r'^unreviewed/$',
        ListUnReviewedTasksView.as_view(),
        name='list_unreviewed_tasks'),
    url(r'^create/$', CreateTaskView.as_view(),
        name='create_task'),
    url(r'^(?P<pk>\d+)/edit/$',
        UpdateTaskView.as_view(), name='edit_task'),
    url(r'^(?P<pk>\d+)/stand_by/$',
        SetTaskStandByView.as_view(),
        name='set_task_standby'),
    url(r'^(?P<pk>\d+)/ready/$',
        SetTaskReadyView.as_view(),
        name='set_task_ready'),
    url(r'^(?P<pk>\d+)/complete/$',
        SetTaskCompletedView.as_view(),
        name='set_task_complete'),
    url(r'report/$',
        ReportHomeView.as_view(),
        name='report_home'),
    url(r'report/task_by_status/json',
        TasksJsonView.as_view(),
        name='task_by_status_json')
]
