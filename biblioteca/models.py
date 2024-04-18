from datetime import timedelta
from django.db import models

# Create your models here.


'''
producto son las especificaciones del libro/producto
Tipus = diferentes tipos de productos del catalogo o del elemento catalogo
Exemplar = cantidad de producto/libro por cada centro
Reserves = usuario pide libro y reserves es la cola para conseguir el libro
Prestecs = usuario se lleva el libro x dias (3 semanas por defecto)
Peticiones = biblioteca pide un libro que le gustaria tener
Logs = tabla de logs
Imatges = ruta de la imagen
Centre = se guardan diferentes centros/bibliotecas
'''

class Producte(models.Model):
    nom = models.CharField(max_length=100)
    cdu = models.CharField(max_length=50)

    autor = models.CharField(max_length=100, blank=True, null=True)
    tipus = models.ForeignKey('Tipus', on_delete=models.CASCADE)

    # Si es un libro
    isbn = models.IntegerField(blank=True, null=True)
    titol = models.CharField(max_length=100, blank=True, null=True)
    signatura = models.CharField(max_length=53, blank=True, null=True)



    def __str__(self):
        return self.nom

class Tipus(models.Model):
    nom = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Tipus"

    def __str__(self):
        return self.nom

class Centre(models.Model):
    nom = models.CharField(max_length=128)

    def __str__(self):
        return self.nom

class Exemplar(models.Model):
    producte = models.ForeignKey('Producte', on_delete=models.CASCADE)
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE)
    quantitat = models.IntegerField()

    def __str__(self):
        return self.producte.nom + ' - ' + self.centre.nom + ' - ' + str(self.quantitat)

class Reserva(models.Model):
    dataReserva = models.DateTimeField(auto_now_add=True)
    producte = models.ForeignKey('Producte', on_delete=models.CASCADE)
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE)
    usuari = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    usuariAdmin = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Reserves"

    def __str__(self):
        return self.producte.nom + ' - ' + self.usuari.username

class Prestec(models.Model):
    dataPrestec = models.DateTimeField(auto_now_add=True)
    dataDevolucio = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.dataPrestec and not self.dataDevolucioMaxima:
            self.dataDevolucioMaxima = self.dataPrestec + timedelta(weeks=3)
        super().save(*args, **kwargs)

    producte = models.ForeignKey('Producte', on_delete=models.CASCADE)
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE)
    usuari = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    usuariAdmin = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    esRetornat = models.BooleanField(default=False)

    def __str__(self):
        return self.producte.nom + ' - ' + self.usuari.username
    
class Peticio(models.Model):
    producte = models.ForeignKey('Producte', on_delete=models.CASCADE)
    centreSolicitant = models.ForeignKey('Centre', on_delete=models.CASCADE)
    centreSolicitat = models.ForeignKey('Centre', on_delete=models.CASCADE)

    dataPeticio = models.DateTimeField(auto_now_add=True)
    usuariAdmin = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Peticions"

    def __str__(self):
        return self.producte.nom + ' - ' + self.usuari.username

class Log(models.Model):
    tipus = models.CharField(max_length=10, choices=[('warning', 'Warning'), ('info', 'Info'), ('error', 'Error'), ('fatal', 'Fatal')])
    informacio = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    usuari = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ruta = models.CharField(max_length=100)

    def __str__(self):
        return self.accio + ' - ' + self.usuari.username