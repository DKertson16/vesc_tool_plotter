from django.contrib import admin

# Register your models here.
from .models import Ride, Build, Board, Foil, Motor, Propeller, Controller, CsvRow

admin.site.register(Ride)
admin.site.register(Build)
admin.site.register(Board)
admin.site.register(Foil)
admin.site.register(Motor)
admin.site.register(Propeller)
admin.site.register(Controller)
admin.site.register(CsvRow)
