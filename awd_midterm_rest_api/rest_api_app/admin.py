from django.contrib import admin
from .models import Protein
from .models import Organism
from .models import Domain
# Register your models here.

admin.site.register(Protein)
admin.site.register(Organism)
admin.site.register(Domain)
