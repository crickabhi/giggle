from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'giggle_app.views.index'), # root
    url(r'^login$', 'giggle_app.views.login_view'), # login
    url(r'^logout$', 'giggle_app.views.logout_view'), # logout
    url(r'^signup$', 'giggle_app.views.signup'), # signup
    url(r'^giggles$', 'giggle_app.views.public'), # public ribbits
    url(r'^submit$', 'giggle_app.views.submit'), # submit new ribbit
	url(r'^users/$', 'giggle_app.views.users'),
    url(r'^users/(?P<username>\w{0,30})/$', 'giggle_app.views.users'),
    url(r'^follow$', 'giggle_app.views.follow'),
    # url(r'^$', 'ribbit.views.home', name='home'),
    # url(r'^ribbit/', include('ribbit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
