from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change,password_change_done
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mj_ranking.views.home', name='home'),
    # url(r'^mj_ranking/', include('mj_ranking.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    (r'^accounts/login/$',  login),
(r'^accounts/logout/$', logout),
(r'^accounts/password/change/$',password_change),
(r'accounts/password/done/$', password_change_done),
)
