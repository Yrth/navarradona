from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import oembed
oembed.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ndona.views.home', name='home'),
    url(r'^adminfiles/', include('adminfiles.urls'), name="adminfiles"),
    url(r'^', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markdown/', include("django_markdown.urls")),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
