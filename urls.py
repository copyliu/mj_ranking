from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change,password_change_done
from mj_ranking import settings
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
(r'^accounts/password/done/$', password_change_done),
   # (r'^leagues/(\d+)/',"mj_ranking.ranking.views.leagues"),
    (r'^$',"mj_ranking.ranking.views.home"),
    (r'import/','mj_ranking.ranking.views.inputresult'),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS[0]}),

    (r"^view/(\d+)/$","mj_ranking.ranking.views.viewleague"),
    (r'^getJSONv2',"mj_ranking.ranking.views.getJSONv2"),
    (r'^getJSON',"mj_ranking.ranking.views.JsonData"),

)
