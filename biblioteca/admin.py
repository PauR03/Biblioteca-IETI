from django.contrib import admin
from .models import Log, Imatge, User, Producte, Llibre, CD, DVD, BR, Dispositiu, Centre, Exemplar, Reserva, Prestec, Peticio

class LogAdmin(admin.ModelAdmin):
    list_display = ('tipus', 'informacio', 'data', 'usuari', 'ruta')  # Los campos que quieres mostrar en la lista
    list_filter = ('tipus', 'usuari')  # Los campos por los que quieres poder filtrar
    search_fields = ('informacio',)  # Los campos en los que quieres poder buscar

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
admin.site.register(Log, LogAdmin)  # Registra Log con la configuración de LogAdmin
admin.site.register(Imatge)