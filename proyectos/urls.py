from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.contrib.auth import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from aplicaciones.new_task.views import CrearActividad
from aplicaciones.new_task.views import UpdateActividad, SetEnCursoView
from aplicaciones.new_task.views import SetTerminadoView, SetTaskView
from aplicaciones.new_task import views as views_new
from aplicaciones.tasks import views as views_task
admin.autodiscover()

urlpatterns = [
    url(r'^$', RedirectView.as_view(
        url='task/'), name='home'),
    url(r'^task/', include('aplicaciones.tasks.urls')),
    url(r'^task/(?P<pk>\d+)/$', UpdateActividad.as_view(),
        name='task_detail'),
    url(r'^(?P<pk>\d+)/encurso/$',
        SetEnCursoView.as_view(),
        name='set_encurso'),
    url(r'^(?P<pk>\d+)/terminado/$',
        SetTerminadoView.as_view(),
        name='set_terminado'),

    url(r'^insert_task/$',
        views_new.insert_new_task, name='insert_new_task'),
    url(r'^insert_user/$',
        views_new.insert_new_user, name='insert_new_user'),
    url(r'^insert_cost/$',
        views_new.insert_new_cost, name='insert_new_cost'),
    url(r'set_task/$', SetTaskView.as_view(),
        name="set_task"),
    url(r'^send_comment/$',
        views_new.send_comment, name='send_comment'),
    url(r'^load_more_comments/$',
        views_new.load_more_comments, name='load_more_comments'),
    url(r'^change_assigned/$',
        views_new.change_assigned, name='change_assigned'),
    url(r'^type_assigned/$',
        views_new.type_assigned, name='type_assigned'),
    url(r'^change_area/$',
        views_new.area_assigned, name='area_assigned'),
    url(r'^change_espired/$',
        views_new.change_espired, name='change_espired'),

    url(r'^pie_actividades/$',
        views_task.pie_actividades, name='pie_actividades'),
    url(r'^bar_encurso/$',
        views_task.bar_encurso, name='bar_encurso'),
    url(r'^bar_terminada/$',
        views_task.bar_terminada, name='bar_terminada'),

    url(r'^get_areas/$',
        views_task.get_areas, name='get_areas'),
    url(r'^get_projects/$',
        views_task.get_projects, name='get_projects'),
    url(r'^get_projects_table/$',
        views_task.get_projects_table, name='get_projects_table'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/',
        include('django_comments.urls')),
    url(r'^accounts/login/$',
        views.login, {'template_name': 'login.html'}, name='login'),

    url(r'^accounts/logout/$',
        views.logout_then_login,
        name='logout'),
    url(r'^tasks/', CrearActividad.as_view(), name='createTask'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
