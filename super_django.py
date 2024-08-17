import os
import functions


c = {
    "r": "\033[91m",
    "g": "\033[92m",
    "y": "\033[93m",
    "b": "\033[94m",
    "w": "\033[97m",
}

print(c['b'] + functions.asci_creator() + c['w'])

#step 0 -install dependencies
if input("Do you want to install dependencies? (y/n): ") == 'y':
    functions.install_req(c)

project_name = input("Enter the name of the project: ")
apps = [input("Enter the name of the app: ")]
while input("Do you want to add another app? (y/n): ") == 'y':
    apps.append(input("Enter the name of the app: "))


settings = {
    "ALLOWED_HOSTS_ALL": input("allow all hosts? (y/n): ") == 'y',
    "CORS_ORIGIN_ALLOW_ALL": input("allow all origins of corsheaders? (y/n): ") == 'y',
    "add_user_model": input(f"Add {project_name.capitalize()}User model (a login system will be created as well)? (y/n): ") == 'y',
}


print(f"creating project {c['b']}{project_name}{c['w']} and {c['b']}{len(apps)} apps{c['w']}...")

#step 1 - create project
os.system(f"python -m django startproject {project_name}")
print(f"{c['g']}Project created")
os.chdir(project_name)

#step 2 - create apps
for app in apps:
    os.system(f"python manage.py startapp {app}")
    print(f"{c['g']}App {app} created")


#step 3 - edit urls.py of project
functions.edit_urls_project(project_name, apps)
print(f"{c['g']}All apps urls added to project urls.py")

#step 4 - edit settings.py of apps
functions.edit_settings_app(project_name, settings, apps)
print(f"{c['g']}All settings added to project settings.py")

#step 5 - delete unnecessary files (we will then create folder to better organize the project)
functions.delete_useless_files(apps)
print(f"{c['g']}All unnecessary files deleted")

#step 6 - create folders
functions.create_usefull_folders_files(apps)
print(f"{c['g']}All necessary folders created")

#step 7 - create models if user wants
if settings["add_user_model"]:
    functions.create_user_model(apps,project_name.capitalize())
    print(f"{c['g']}User model created")

#step 8 - create runner
functions.create_runner()
print(f"{c['g']}Runner created")


print(f"\n{c['w']}Project {c['b']}{project_name}{c['w']} and {c['b']}{len(apps)} apps{c['w']} created {c['g']}successfully{c['w']}!")
