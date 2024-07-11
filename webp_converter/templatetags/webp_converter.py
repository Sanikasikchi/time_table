from django.shortcuts import render
from backend.baseapp.templatetags import helper
from django import template
from django.templatetags.static import static
from django.core.cache import cache

from webp_converter.utils import make_image_key
from webp_converter.models import WebPImage
from backend.baseapp.templatetags import helper

register = template.Library()


@register.simple_tag(takes_context=True)
def static_webp(context, static_path, webptype=0):

    if static_path[0] == '/':
        static_path = static_path.replace('/media', 'media')
        
    quality = 80
    try:
        webp_compatible = context["webp_compatible"]
    except KeyError:
        raise Exception(
            "'webp_converter.context_processors.webp_support' "
            "needs to be added to your context processors."
        )
    if not webp_compatible:
        webp_image_url = helper.image_absolute_path(static_path)
        return return_response(webptype, webp_image_url, static_path)

    try:
        key = make_image_key(static_path, quality)
        webp_image_url = cache.get(key)
        if not webp_image_url:
            webp_image, _ = WebPImage.objects.get_or_create(
                static_path=static_path, quality=quality
            )
            if not webp_image.webp_image_exists:
                webp_image.save_webp_image()
            webp_image_url = webp_image.webp_url
            cache.set(key, webp_image_url)
    except Exception as err:
        webp_image_url = helper.image_absolute_path(static_path)

    return return_response(webptype, webp_image_url, static_path)


def return_response(webptype, webp_image_url, static_path):
    if webptype == 0:
        tmpl = template.loader.get_template("picture.html")
        return tmpl.render({
            "webp": webp_image_url,
            "jpeg": helper.image_absolute_path(static_path),
        })
    else:
        return webp_image_url
