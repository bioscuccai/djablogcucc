from django.conf.urls import url, patterns

from blogcucc import views

urlpatterns=patterns('',
    url(r'^$', views.BejegyzesList.as_view(), name="blogcucc_bejegyzeslist"),
    url(r'^cimke/(?P<cimke>\w+)/$', views.BejegyzesByCimke.as_view(), name="blogcucc_cimke"),
    url(r'^datum/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.BejegyzesHonap.as_view(month_format='%m'), name="blogcucc_datum"),
    url(r'^addbejegyzes/$', views.BejegyzesCreate.as_view(), name="blogcucc_addbejegyzes"),
    url(r'^detailbejegyzes/(?P<pk>\d+)/$', views.BejegyzesDetail.as_view(), name="blogcucc_detailbejegyzes"),
    url(r'^editbejegyzes/(?P<pk>\d+)/$', views.BejegyzesUpdate.as_view(), name="blogcucc_editbejegyzes"),
    url(r'^addcimke/$', views.CimkeCreate.as_view(), name="blogcucc_addcimke"),
    url(r'addkomment/(?P<bejegyzes>\d+)/$', views.KommentCreate.as_view(), name="blogcucc_addkomment"),

)