from django.contrib import admin
from .models import Log, User, Producte, Llibre, CD, DVD, BR, Dispositiu, Centre, Exemplar, Reserva, Prestec, Peticio

class LogAdmin(admin.ModelAdmin):
    list_display = ('tipus', 'informacio', 'data', 'get_full_name', 'ruta')  # Los campos que quieres mostrar en la lista
    list_filter = ('tipus', 'usuari')  # Los campos por los que quieres poder filtrar
    search_fields = ('informacio',)  # Los campos en los que quieres poder buscar

    def get_full_name(self, obj):
        return obj.usuari.first_name + ' ' + obj.usuari.last_name
    get_full_name.short_description = 'Nombre completo'  # Etiqueta para la columna



class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('producte', 'centre', 'quantitat')




# Registra tus modelos aquí.
admin.site.register(User)
admin.site.register(Producte)
admin.site.register(Llibre)
admin.site.register(CD)
admin.site.register(DVD)
admin.site.register(BR)
admin.site.register(Dispositiu)
admin.site.register(Centre)
admin.site.register(Exemplar, ExemplarAdmin)
#admin.site.register(Exemplar)
admin.site.register(Reserva)
admin.site.register(Prestec)
admin.site.register(Peticio)
admin.site.register(Log, LogAdmin) 