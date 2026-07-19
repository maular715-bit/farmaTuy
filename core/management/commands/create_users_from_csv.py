from django.core.management.base import BaseCommand, CommandError
import csv
from pathlib import Path


class Command(BaseCommand):
    help = 'Crear usuarios (AuthUsuario + Usuario) desde un CSV con columnas: identifier,username,email,role'

    def add_arguments(self, parser):
        parser.add_argument('file', help='CSV path')
        parser.add_argument('--default-password', dest='default_password', help='Password por defecto para nuevos usuarios', default='changeme123')
        parser.add_argument('--dry-run', action='store_true', help='Mostrar acciones sin guardar')

    def handle(self, *args, **options):
        file = options['file']
        dry = options.get('dry_run')
        default_password = options.get('default_password')

        from core.models import Usuario, AuthUsuario
        from core.auth_utils import hash_password

        p = Path(file)
        if not p.exists():
            raise CommandError(f'File not found: {file}')

        created = 0
        with p.open(newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                username = (row.get('username') or '').strip()
                email = (row.get('email') or '').strip()
                role = (row.get('role') or '').strip() or Usuario.ROLE_FARMACIA
                if not username:
                    self.stdout.write(self.style.ERROR(f'Skipping row without username/email: {row}'))
                    continue

                # Skip if exists
                if Usuario.objects.filter(username=username).exists():
                    self.stdout.write(self.style.NOTICE(f'Exists: {username}'))
                    continue

                self.stdout.write(self.style.NOTICE(f'Will create: {username} ({email}) role={role} (dry-run={dry})'))
                if not dry:
                    pwd_hash = hash_password(default_password)
                    auth = AuthUsuario.objects.create(correo=email or f'{username}@noemail', password_hash=pwd_hash)
                    Usuario.objects.create(auth_usuario=auth, username=username, role=role)
                    created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created} users'))