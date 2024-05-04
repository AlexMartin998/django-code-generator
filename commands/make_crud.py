import os
import shutil
from typing import List, Optional

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the app."

    parent_target_path = None
    model_name = None

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

        parser.add_argument(
            "--model_name", type=str, help="The name of the model.", required=True
        )

    def handle(self, *args, **options):
        is_new_app = options["create_app"]
        new_app_name = options["app_name"]
        self.parent_target_path = f"./{new_app_name}"

        model_name = options["model_name"]
        self.model_name = model_name

        if is_new_app:
            self.handle_app_creation(new_app_name)
        else:
            print("Creating only model in existing app")

    def handle_app_creation(self, app_name):
        exist_app = os.path.exists(self.parent_target_path)

        if exist_app:
            self.remove_django_app(app_name)
        else:
            self.create_django_app(app_name)

    # ####  Methods ========================
    # ##  Create the app ----------------
    def create_django_app(self, app_name):
        os.system(f"python manage.py startapp {app_name}")
        print(f"Created: {app_name}")

        # ## upd settings.py ------
        self.update_settings(app_name)

        # # Remove the files that are not needed
        target_path = self.parent_target_path
        paths_to_remove = [
            "views.py",
            "models.py",
            "tests.py",
        ]
        self.remove_several_files(self.parent_target_path, paths_to_remove)

        # # Create the files and folders
        self.create_initial_files(app_name, self.model_name)

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

        # ## recreate the app
        self.create_django_app(app_name)

    # ##  Create initial files ----------------
    def create_initial_files(self, app_name, model_name):
        # ## Create the files and folders
        self.parent_target_path
        paths_to_create = [
            "filters",
            "models",
            "serializers",
            "urls",
            "views",
        ]
        for path in paths_to_create:
            os.makedirs(f"{self.parent_target_path}/{path}", exist_ok=True)
            print(f"Created dir: {path}")

        # ## Create the files
        files_to_create = [
            f"{self.parent_target_path}/filters/__init__.py",
            f"{self.parent_target_path}/models/__init__.py",
            f"{self.parent_target_path}/serializers/__init__.py",
            f"{self.parent_target_path}/urls/__init__.py",
            f"{self.parent_target_path}/views/__init__.py",
        ]
        for file in files_to_create:
            with open(file, "w") as f:
                f.write("# autogenerated file\n")
            print(f"Created file: {file}")

        # ## Create the model file
        self.create_model_file(app_name, model_name)

    # ##  Create the model file ----------------
    def create_model_file(self, app_name, model_name):
        model_file_name = self.calc_filename(model_name) + "_model.py"
        model_file = f"{self.parent_target_path}/models/{model_file_name}"
        with open(model_file, "w") as f:
            f.write(
                f"from django.db import models\n\n\nclass {model_name}(models.Model):\n    pass\n"
            )
        print(f"Created file: {model_file}")

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

    def calc_filename(self, name: str) -> str:
        name = name.replace(" ", "_")
        name = name[0].lower() + name[1:]
        i = 0
        while i < len(name):
            if name[i].isupper():
                name = name[:i] + "_" + name[i].lower() + name[i + 1 :]
                i += 1  # Skip the underscore on the next iteration
            i += 1
        return name
