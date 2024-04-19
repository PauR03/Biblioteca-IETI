from django.contrib import admin
from .models import User, Producte, Llibre, CD, DVD, BR, Dispositiu, Centre, Exemplar, Reserva, Prestec, Peticio, Log, Imatge

# Registra tus modelos aquí.
admin.site.register(User)
admin.site.register(Producte)
admin.site.register(Llibre)
admin.site.register(CD)
admin.site.register(DVD)
admin.site.register(BR)
admin.site.register(Dispositiu)
admin.site.register(Centre)
admin.site.register(Exemplar)
admin.site.register(Reserva)
admin.site.register(Prestec)
admin.site.register(Peticio)
admin.site.register(Log)
admin.site.register(Imatge)