from django.contrib.syndication.views import Feed
from .models import Entry

class LatestPost(Feed):
    title = "NavarraDona Blog"
    link = "/feed/"
    description = "Ultimos Posts de NavarraDona"

    def items(self):
        return Entry.objects.published()[:5]
