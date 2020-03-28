import sys, os, django
sys.path.append('/system/coronaproj/coronaliveapp/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coronaliveapp.settings")
django.setup()

from corona.models import Cache
cache = Cache.objects.get(cache_key = 'homepage')
print(cache.data)