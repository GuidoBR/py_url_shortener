from django.db import models
from django.core.urlresolvers import reverse
from .basechanger import decimal2base_n, base_n2decimal


class Link(models.Model):
    url = models.URLField()

    @staticmethod
    def encurtar(link):
        l, _ = Link.objects.get_or_create(url=link.url)
        return str(decimal2base_n(l.pk))

    @staticmethod
    def expandir(slug):
        link_id = int(base_n2decimal(slug))
        l = Link.objects.get(pk=link_id)
        return l.url

    def get_absolute_url(self):
        return reverse("link_show", kwargs={"pk": self.pk})

    def url_curta(self):
        return reverse("redirect_short_url",
                       kwargs={"short_url": Link.encurtar(self)})
