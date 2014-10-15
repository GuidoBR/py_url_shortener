from django.db import models

class Link(models.Model):
    url = models.URLField()

    @staticmethod
    def encurtar(link):
        l, _ = Link.objects.get_or_create(url=link.url)
        return str(l.pk)

    @staticmethod
    def expandir(slug):
        link_id = int(slug)
        l = Link.objects.get(pk=link_id)
        return l.url