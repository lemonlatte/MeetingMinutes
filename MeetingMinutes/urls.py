from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'MeetingMinutes.views.home', name='home'),
    url(r'^list$', 'MeetingMinutes.views.list_meetings', name='list'),
    url(r'^add$', 'MeetingMinutes.views.add_meeting', name='add'),
    url(r'^delete$', 'MeetingMinutes.views.del_meeting', name='delete'),
    url(r'^(?P<_id>\w+)/add$', 'MeetingMinutes.views.add_minute', name='add_minute'),
    url(r'^(?P<_id>\w+)/delete$', 'MeetingMinutes.views.del_minute', name='delete_minute'),
    url(r'^login$', 'account.views.login', name='login'),
    url(r'^logout$', 'account.views.logout', name='logout'),
    # url(r'^MeetingMinutes/', include('MeetingMinutes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
