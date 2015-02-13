from django.conf.urls import patterns, include, url
from . import views, feed

urlpatterns = patterns(
        '',
        url(r'^blog/create_post/', feed.LatestPost(), name="entry_detai22l"),
        url(r'^blog/entry/(?P<slug>\S+)/', views.BlogDetail.as_view(), name="entry_detail"),
        url(r'^blog/feed/', feed.LatestPost(), name="feed"),
        url(r'^blog/?(?P<page>\d+)?', views.BlogIndex.as_view(), name="index"),
        url(r'^partners/', views.Partners.as_view(), name="partners"),
        url(r'^$', views.PageIndex.as_view(), name="page_index"),
        
    )