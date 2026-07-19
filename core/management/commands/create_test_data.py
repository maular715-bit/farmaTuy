from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create test Tipos and Farmacia'

    def handle(self, *args, **options):
        from core.models import Tipo, Farmacia
        p1, _ = Tipo.objects.get_or_create(nombre='Principio A', defaults={'descripcion':'Principio activo A'})
        p2, _ = Tipo.objects.get_or_create(nombre='Presentacion X', defaults={'descripcion':'Caja 10'})
        f, _ = Farmacia.objects.get_or_create(razon_social='Farmacia Uno', defaults={'rif':'J-0001','estado':'Estado','municipio':'Municipio','parroquia':'Parroquia','correo':'farmacia1@example.com'})
        self.stdout.write(f'TIPO_PRINCIPIO_ID {p1.id}')
        self.stdout.write(f'TIPO_PRESENTACION_ID {p2.id}')
        self.stdout.write(f'FARMACIA_ID {f.id}')
