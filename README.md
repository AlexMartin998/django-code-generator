# Django Command: make_crud

This Django command allows you to create and delete Django applications.

## Usage

To use this command, run the following command in your terminal:

```bash

# create new app from scratch
python manage.py make_crud --create_app --app_name="books" --model_name="Book"

# add model to an existing directory
python manage.py make_crud --app_name="books" --model_name="Author"

```

### Arguments

`--create_app`: This argument is optional. If provided, the command will create a new Django application.
`--app_name`: This argument is required if --create_app is provided. It specifies the name of the new Django application to create.

### Functions

- `create_django_app(app_name)`: Creates a new Django application with the provided name and adds it to INSTALLED_APPS in settings.py.
- `remove_django_app(app_name)`: Deletes the Django application with the provided name and removes it from INSTALLED_APPS in settings.py.
- `update_settings(app_name, isCreatingApp)`: Updates INSTALLED_APPS in settings.py to add or remove the specified application.
- `remove_dir(path)`: Deletes the directory at the specified path.
- `remove_several_files(path, files)`: Deletes several files at the specified path.
  Notes
