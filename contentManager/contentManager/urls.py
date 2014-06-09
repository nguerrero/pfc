from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('manager.views',
    # Examples:
    # url(r'^$', 'contentManager.views.home', name='home'),
    # url(r'^contentManager/', include('contentManager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # ======================== ADMIN URLS ==============================
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # ========================= MAIN PAGE ==============================
    (r'^ultimos$', 'search'),
	(r'^streaming$', 'stream'),
	(r'^statistics$', 'statistics'),
	(r'^statistics/rt$', 'rtStatistics'),
	(r'^statistics/user$', 'userStatistics'),
	(r'^statistics/popular$', 'popularStatistics'),
	(r'^statistics/ht$', 'htStatistics'),
	(r'^statistics/dates$', 'datesStatistics'),
	(r'^statistics/year$', 'yearStatistics'),
	(r'^statistics/prueba$', 'prueba'),
    #(r'^feed/(.*)$','SelectedEntriesFeed'),
    #(r'^(.*)$', 'show_error',
    (r'^', 'stream'),
)
