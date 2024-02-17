from django.core.management.base import BaseCommand
from open_problems.models.open_problems import OpenProblems


class Command(BaseCommand):
    help = 'Update the descendants count for all OpenProblems'

    def handle(self, *args, **options):
        OpenProblems.update_descendants_count()
        self.stdout.write(self.style.SUCCESS('Successfully updated descendants count'))
