from .models import Category

#As we have made context processors file, we need to pass entry in settings.py file under Templates/
#It will be available for all templates

#context processors is to automatically get stuff for all categories option(dropdown)
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
