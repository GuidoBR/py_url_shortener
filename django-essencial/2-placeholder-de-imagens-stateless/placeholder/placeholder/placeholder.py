from django import forms
from django.core.cache import cache
from io import BytesIO
from PIL import Image, ImageDraw


class ImageForm(forms.Form):
    """ Form para validar as dimensões do placeholder solicitado """
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):
        """ Gera uma imagem no tamanho e tipo especificados.
        Retorna bytes """
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if not content:
            image = Image.new('RGB', (width, height))

            draw = ImageDraw.Draw(image)
            text = '{} x {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) / 2
                textleft = (width - textwidth) / 2
                draw.text((textleft, texttop), text, fill=(255, 255, 255))

            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60*60)
        return content
