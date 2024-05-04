import os
import shutil
from typing import List, Optional

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the app."

    def add_arguments(self, parser):
        parser.add_argument(
            "--create_app",
            action="store_true",
            help="Create the app.",
            default=False,
            required=False,
        )
        parser.add_argument(
            "--app_name", type=str, help="The name of the app.", required=False
        )

    def handle(self, *args, **options):
        is_new_app = options["create_app"]
        new_app_name = options["app_name"]

        if is_new_app:
            self.handle_app_creation(new_app_name)
        else:
            print("Creating model")

    def handle_app_creation(self, app_name):
        target_path = f"./{app_name}"
        exist_app = os.path.exists(target_path)

        if exist_app:
            self.remove_django_app(app_name)
        else:
            self.create_django_app(app_name)

    # ####  Methods ========================
    # ##  Create the app ----------------
    def create_django_app(self, app_name):
        os.system(f"python manage.py startapp {app_name}")
        print(f"Created: {app_name}")

        # ## upd settings.py
        self.update_settings(app_name)

    def update_settings(self, app_name: str, isCreatingApp: Optional[bool] = True):
        settings_path = "./backend/settings.py"
        with open(settings_path, "r") as file:
            lines = file.readlines()

        # ## Add the app to the INSTALLED_APPS ------
        if isCreatingApp:
            app_line = f"    '{app_name}',\n"
            # search line that contains "# own django apps" and save the index
            start_index = 0
            for i, line in enumerate(lines):
                if "# own django apps" in line:
                    start_index = i
                    break

            # search for the closing bracket from the start_index
            for i, line in enumerate(lines[start_index:], start=start_index):
                if "]" in line:
                    lines.insert(i, app_line)
                    break

            # ## Write the changes
            with open(settings_path, "w") as file:
                file.writelines(lines)
            print(f"Updated: {settings_path}")
        else:
            # ## Remove the app from the INSTALLED_APPS ------
            start_index = 0
            end_index = 0
            for i, line in enumerate(lines):
                if app_name in line:
                    start_index = i
                    break

            for i, line in enumerate(lines[start_index:], start=start_index):
                if "]" in line:
                    end_index = i
                    break

            del lines[start_index:end_index]

            # ## Write the changes
            with open(settings_path, "w") as file:
                file.writelines(lines)
            print(f"Updated: {settings_path}")

    # ##  Remove the app ----------------
    def remove_django_app(self, app_name):
        self.remove_dir(f"./{app_name}")

        # ## upd settings.py
        self.update_settings(app_name, isCreatingApp=False)

    # ####  Aux Functions ========================
    def remove_dir(self, path):
        try:
            shutil.rmtree(path)
            print(f"Removed dir: {path}")
        except OSError as e:
            print(f"Error: {e.strerror}")

    def remove_several_files(self, path, files: List[str]):
        for file in files:
            try:
                os.remove(f"{path}/{file}")
                print(f"Removed file: {file}")
            except OSError as e:
                print(f"Error: {e.strerror}")
