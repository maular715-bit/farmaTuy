from django.core.management.base import BaseCommand, CommandError
from core.models import Usuario
import csv


class Command(BaseCommand):
    help = 'Asignar roles a usuarios. Uso: --all ROLE  |  --user USER ROLE  |  --file path.csv'

    def add_arguments(self, parser):
        parser.add_argument('--all', dest='role_all', help='Asignar ROLE a todos los usuarios')
        parser.add_argument('--user', nargs=2, metavar=('USERNAME', 'ROLE'), help='Asignar ROLE a un usuario (por username)')
        parser.add_argument('--file', dest='file', help='CSV con username_or_email,role por línea')
        parser.add_argument('--dry-run', action='store_true', help='Mostrar acciones sin guardar')

    def handle(self, *args, **options):
        role_choices = [c[0] for c in Usuario.ROLE_CHOICES]
        dry = options.get('dry_run') or options.get('dry-run') or options.get('dry_run')

        if options.get('role_all'):
            role = options['role_all']
            if role not in role_choices:
                raise CommandError(f'Rol inválido. Opciones: {role_choices}')
            qs = Usuario.objects.all()
            self.stdout.write(self.style.NOTICE(f'Asignando role="{role}" a {qs.count()} usuarios (dry-run={dry})'))
            if not dry:
                qs.update(role=role)
            return

        if options.get('user'):
            username, role = options.get('user')
            if role not in role_choices:
                raise CommandError(f'Rol inválido. Opciones: {role_choices}')
            try:
                u = Usuario.objects.get(username=username)
            except Usuario.DoesNotExist:
                raise CommandError(f'Usuario no encontrado: {username}')
            self.stdout.write(self.style.NOTICE(f'Usuario: {u.username} -> role {role} (dry-run={dry})'))
            if not dry:
                u.role = role
                u.save()
            return

        if options.get('file'):
            path = options['file']
            updated = 0
            with open(path, newline='', encoding='utf-8') as fh:
                reader = csv.reader(fh)
                for row in reader:
                    if not row:
                        continue
                    identifier = row[0].strip()
                    role = row[1].strip() if len(row) > 1 else ''
                    if role not in role_choices:
                        self.stdout.write(self.style.ERROR(f'Skipping {identifier}: rol inválido "{role}"'))
                        continue
                    # try by username then by auth email
                    u = Usuario.objects.filter(username=identifier).first()
                    if not u:
                        # try by auth email
                        u = Usuario.objects.filter(auth_usuario__correo=identifier).first()
                    if not u:
                        self.stdout.write(self.style.ERROR(f'Usuario no encontrado: {identifier}'))
                        continue
                    self.stdout.write(self.style.NOTICE(f'{u.username}: {u.role} -> {role} (dry-run={dry})'))
                    if not dry:
                        u.role = role
                        u.save()
                        updated += 1
            self.stdout.write(self.style.SUCCESS(f'Updated {updated} users'))
            return

        raise CommandError('No se especificó ninguna acción. Usa --help para ver opciones.')
