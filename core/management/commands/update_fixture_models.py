import json
from typing import Any, Dict, List

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    A Django management command to update model references in a fixture file.

    This command changes the app label for models in a given fixture file, making it
    possible to load data into the same model structure located in a different app.

    Usage:
        python manage.py update_fixture_models <fixture_file_path> <old_app_label> <new_app_label>

    Example:
        python manage.py update_fixture_models data.json my_old_app my_new_app
    """

    help = "Updates model references in a Django fixture file from one app to another."

    def add_arguments(self, parser) -> None:
        """
        Adds command-line arguments for the management command.
        """
        parser.add_argument("fixture_file", type=str, help="Path to the fixture file")
        parser.add_argument("old_app", type=str, help="Old app label")
        parser.add_argument("new_app", type=str, help="New app label")

    def handle(self, *args, **options) -> None:
        """
        The main command logic, reading the fixture file, updating references, and writing changes.
        """
        fixture_file: str = options["fixture_file"]
        old_app: str = options["old_app"]
        new_app: str = options["new_app"]

        try:
            # Load the fixture data
            with open(fixture_file, "r") as file:
                data: List[Dict[str, Any]] = json.load(file)

            # Update the model references
            updated: bool = False
            for obj in data:
                if obj["model"].startswith(f"{old_app}."):
                    obj["model"] = obj["model"].replace(old_app, new_app, 1)
                    updated = True

            # Save the updated fixture data if changes were made
            if updated:
                with open(fixture_file, "w") as file:
                    json.dump(data, file, indent=4)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully updated model references in "{fixture_file}"'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING("No model references were updated.")
                )

        except FileNotFoundError:
            raise CommandError(f'File "{fixture_file}" does not exist.')
        except json.JSONDecodeError:
            raise CommandError(f'Error decoding JSON from "{fixture_file}".')
