from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Crea los grupos básicos: Administrador, Veterinario, Cliente'

    def handle(self, *args, **options):
        grupos = ['administrador', 'veterinario', 'cliente']
        created = []
        for g in grupos:
            group, ok = Group.objects.get_or_create(name=g)
            if ok:
                created.append(g)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Grupos creados: {created}'))
        else:
            self.stdout.write('Los grupos ya existían')
