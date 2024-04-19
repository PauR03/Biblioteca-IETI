# Generated by Django 5.0.4 on 2024-04-19 14:37

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titol', models.CharField(max_length=100)),
                ('descripcio', models.TextField()),
                ('autor', models.CharField(blank=True, max_length=100, null=True)),
                ('data_edicio', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Imatge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruta', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BR',
            fields=[
                ('producte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='biblioteca.producte')),
                ('duracio', models.IntegerField()),
            ],
            bases=('biblioteca.producte',),
        ),
        migrations.CreateModel(
            name='CD',
            fields=[
                ('producte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='biblioteca.producte')),
                ('discrografia', models.CharField(max_length=100)),
                ('estil', models.CharField(max_length=100)),
                ('duracio', models.IntegerField()),
            ],
            bases=('biblioteca.producte',),
        ),
        migrations.CreateModel(
            name='Dispositiu',
            fields=[
                ('producte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='biblioteca.producte')),
                ('marca', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            bases=('biblioteca.producte',),
        ),
        migrations.CreateModel(
            name='DVD',
            fields=[
                ('producte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='biblioteca.producte')),
                ('duracio', models.IntegerField()),
            ],
            bases=('biblioteca.producte',),
        ),
        migrations.CreateModel(
            name='Llibre',
            fields=[
                ('producte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='biblioteca.producte')),
                ('cdu', models.CharField(max_length=50)),
                ('isbn', models.IntegerField()),
                ('editorial', models.CharField(max_length=100)),
                ('colleccio', models.CharField(max_length=100)),
                ('pagines', models.IntegerField()),
                ('signatura', models.CharField(blank=True, max_length=53, null=True)),
            ],
            bases=('biblioteca.producte',),
        ),
        migrations.CreateModel(
            name='Exemplar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantitat', models.IntegerField()),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.centre')),
                ('producte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.producte')),
            ],
        ),
        migrations.AddField(
            model_name='producte',
            name='idImatge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biblioteca.imatge'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('esAdmin', models.BooleanField(default=False)),
                ('dataNaixement', models.DateField(blank=True, null=True)),
                ('centre', models.CharField(blank=True, max_length=100, null=True)),
                ('cicle', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('imatgePerfil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biblioteca.imatge')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipus', models.CharField(choices=[('warning', 'Warning'), ('info', 'Info'), ('error', 'Error'), ('fatal', 'Fatal')], max_length=10)),
                ('informacio', models.TextField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('ruta', models.CharField(max_length=100)),
                ('usuari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Peticio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataPeticio', models.DateTimeField(auto_now_add=True)),
                ('centreSolicitant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peticio_solicitant', to='biblioteca.centre')),
                ('centreSolicitat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peticio_solcitat', to='biblioteca.centre')),
                ('producte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.producte')),
                ('usuariAdmin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Peticions',
            },
        ),
        migrations.CreateModel(
            name='Prestec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataPrestec', models.DateTimeField(auto_now_add=True)),
                ('dataDevolucio', models.DateTimeField(blank=True, null=True)),
                ('esRetornat', models.BooleanField(default=False)),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.centre')),
                ('producte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.producte')),
                ('usuari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestec_usuari', to=settings.AUTH_USER_MODEL)),
                ('usuariAdmin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestec_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataReserva', models.DateTimeField(auto_now_add=True)),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.centre')),
                ('producte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.producte')),
                ('usuari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserva_usuari', to=settings.AUTH_USER_MODEL)),
                ('usuariAdmin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserva_admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reserves',
            },
        ),
    ]
