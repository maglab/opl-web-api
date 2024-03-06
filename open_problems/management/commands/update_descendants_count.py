from django.core.management.base import BaseCommand

from open_problems.models.open_problems import OpenProblem


class Command(BaseCommand):
    help = "Update the descendants count for all OpenProblems"

    def handle(self, *args, **options):
        OpenProblem.update_descendants_count()
        self.stdout.write(self.style.SUCCESS("Successfully updated descendants count"))
