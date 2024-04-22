from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# from django.contrib.auth.models import User



class User(AbstractUser):
    esAdmin = models.BooleanField(default=False)
    dataNaixement = models.DateField(null=True, blank=True)
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE, null=True, blank=True)
    cicle = models.CharField(max_length=100, null=True, blank=True)
    imatgePerfil = models.ImageField(upload_to='imatgePerfil/', default='imatgePerfil/default.jpg')
 
class Producte(models.Model):
    titol = models.CharField(max_length=100)
    descripcio = models.TextField()
    autor = models.CharField(max_length=100, blank=True, null=True)
    data_edicio = models.DateField()
    idImatge = models.ForeignKey('Imatge', on_delete=models.CASCADE, blank=True, null=True)

    
class Llibre(Producte):
    cdu = models.CharField(max_length=50)
    isbn = models.BigIntegerField()
    editorial = models.CharField(max_length=100)
    colleccio = models.CharField(max_length=100)
    pagines = models.IntegerField()
    signatura = models.CharField(max_length=53, blank=True, null=True)

    def __str__(self):
        return self.titol

class CD(Producte):
    discrografia = models.CharField(max_length=100)
    estil = models.CharField(max_length=100)
    duracio = models.IntegerField()

    def __str__(self):
        return self.titol
    
class DVD(Producte):
    duracio = models.IntegerField()

    def __str__(self):
        return self.titol

class BR(Producte):
    duracio = models.IntegerField()

    def __str__(self):
        return self.titol

class Dispositiu(Producte):
    marca = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.titol

class Centre(models.Model):
    nom = models.CharField(max_length=128)

    def __str__(self):
        return self.nom

class Exemplar(models.Model):
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    quantitat = models.IntegerField()

    def __str__(self):
        return self.producte.nom + ' - ' + self.centre.nom + ' - ' + str(self.quantitat)

class Reserva(models.Model):
    dataReserva = models.DateTimeField(auto_now_add=True)
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    usuari = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reserva_usuari")
    usuariAdmin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reserva_admin")

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

    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    usuari = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prestec_usuari")
    usuariAdmin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prestec_admin")
    esRetornat = models.BooleanField(default=False)

    def __str__(self):
        return self.producte.nom + ' - ' + self.usuari.username
    
class Peticio(models.Model):
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    centreSolicitant = models.ForeignKey(Centre, on_delete=models.CASCADE, related_name="peticio_solicitant")
    centreSolicitat = models.ForeignKey(Centre, on_delete=models.CASCADE, related_name="peticio_solcitat")

    dataPeticio = models.DateTimeField(auto_now_add=True)
    usuariAdmin = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Peticions"

    def __str__(self):
        return self.producte.nom + ' - ' + self.usuari.username

class Log(models.Model):
    tipus = models.CharField(max_length=10, choices=[('warning', 'Warning'), ('info', 'Info'), ('error', 'Error'), ('fatal', 'Fatal')])
    informacio = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    usuari = models.ForeignKey(User, on_delete=models.CASCADE)
    ruta = models.CharField(max_length=100)

    def __str__(self):
        return self.accio + ' - ' + self.usuari.username
    
class Imatge(models.Model):
    ruta = models.CharField(max_length=100)
