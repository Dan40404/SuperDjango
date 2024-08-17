
import os


def install_req(c):
    # step 0 -install dependencies
    requirements = [
        "Django",
        "djangorestframework",
        "django-cors-headers",
    ]

    print(f"{c['b']}Installing dependencies...")

    for requirement in requirements:

        if os.system(f"pip show {requirement} -q") == 0:
            print(f"{c['g']}Requirement {requirement} already installed")
            continue

        os.system(f"pip install -q {requirement}")
        print(f"{c['g']}Installed {requirement}")
    print("", c['w'])


def edit_urls_project(project_name, apps):
    base_file = open(f"{project_name}/urls.py", "r", encoding="utf-8").read()
    base_file = base_file.replace("from django.urls import path", "from django.urls import path\nfrom django.urls.conf import include")

    old_urlpatterns = "path('admin/', admin.site.urls),"
    new_urlpatterns = old_urlpatterns
    for app in apps:
        new_urlpatterns += f"\n    path('{app}/', include('{app}.urls')),"

    base_file = base_file.replace(old_urlpatterns, new_urlpatterns)

    open(f"{project_name}/urls.py", "w", encoding="utf-8").write(base_file)


def edit_settings_app(project_name, settings, apps):

    base_file = open(f"{project_name}/settings.py", "r", encoding="utf-8").read()

    # ALLOWED_HOSTS & CORS_ORIGIN_ALLOW_ALL
    allowed_hosts = "*" if settings["ALLOWED_HOSTS_ALL"] else ""
    cors_origin_allow_all = "True" if settings["CORS_ORIGIN_ALLOW_ALL"] else "False"
    cors_allow_headers =  "[\n'content-type',\n 'Content-Type',\n 'token',\n 'email',\n 'password',\n]" if settings["add_user_model"] else  "[\n'content-type',\n 'Content-Type',\n]"
    base_file = base_file.replace("ALLOWED_HOSTS = []", f"ALLOWED_HOSTS = ['{allowed_hosts}']\n\nCORS_ORIGIN_ALLOW_ALL = {cors_origin_allow_all}\n\nCORS_ALLOW_HEADERS = {cors_allow_headers}")

    # INSTALLED_APPS
    old_installed_apps = "'django.contrib.staticfiles',"
    new_installed_apps = old_installed_apps
    for app in apps:
        new_installed_apps += f"\n    '{app}',"
    new_installed_apps += "\n    'rest_framework',"
    new_installed_apps += "\n    'corsheaders',"
    base_file = base_file.replace(old_installed_apps, new_installed_apps)

    # MIDDLEWARE
    base_file = base_file.replace("'django.middleware.csrf.CsrfViewMiddleware',", "'django.middleware.csrf.CsrfViewMiddleware',\n    'corsheaders.middleware.CorsMiddleware',")

    # TIMEZONE

    base_file = base_file.replace("TIME_ZONE = 'UTC'", """TIME_ZONE = "Africa/Bangui" if datetime.datetime.now().astimezone().tzinfo.utcoffset(datetime.datetime.now()).seconds/3600 == 1 else "US/Eastern" """)
    base_file = base_file.replace("from pathlib import Path", "from pathlib import Path\nimport datetime")

    open(f"{project_name}/settings.py", "w", encoding="utf-8").write(base_file)


def delete_useless_files(apps):

    to_delete = [
        "models.py",
        "views.py",
        "tests.py",
    ]

    for app in apps:
        for file in to_delete:
            os.remove(f"{app}/{file}")


def create_usefull_folders_files(apps):

    to_create = [
        "models",
        "views",
        "serializers",
        "tests",
        "tools",
    ]

    for app in apps:

        for folder in to_create:
            os.mkdir(f"{app}/{folder}")
            open(f"{app}/{folder}/__init__.py", "w").write("")

            if folder == "models":
                open(f"{app}/models/base_models.py", "w",encoding="utf-8").write("from django.db import models")

            if folder == "views":
                open(f"{app}/views/base_views.py", "w",encoding="utf-8").write("from django.http import HttpResponse\nfrom rest_framework.views import APIView\nfrom rest_framework.response import Response")

            if folder == "serializers":
                open(f"{app}/serializers/base_serializers.py", "w",encoding="utf-8").write("from rest_framework import serializers")

        open(f"{app}/urls.py", "w",encoding="utf-8").write(f"from django.urls import path\n\nurlpatterns = [\n\n]")


def asci_creator():
    return """
 __       __                  __                  __                        _______                               ______          
/  \     /  |                /  |                /  |                      /       \                             /      \         
$$  \   /$$ |  ______    ____$$ |  ______        $$ |____   __    __       $$$$$$$  |  ______   _______         /$$$$$$  |______  
$$$  \ /$$$ | /      \  /    $$ | /      \       $$      \ /  |  /  |      $$ |  $$ | /      \ /       \        $$ |_ $$//      \ 
$$$$  /$$$$ | $$$$$$  |/$$$$$$$ |/$$$$$$  |      $$$$$$$  |$$ |  $$ |      $$ |  $$ | $$$$$$  |$$$$$$$  |       $$   |  /$$$$$$  |
$$ $$ $$/$$ | /    $$ |$$ |  $$ |$$    $$ |      $$ |  $$ |$$ |  $$ |      $$ |  $$ | /    $$ |$$ |  $$ |       $$$$/   $$ |  $$/ 
$$ |$$$/ $$ |/$$$$$$$ |$$ \__$$ |$$$$$$$$/       $$ |__$$ |$$ \__$$ |      $$ |__$$ |/$$$$$$$ |$$ |  $$ |       $$ |    $$ |      
$$ | $/  $$ |$$    $$ |$$    $$ |$$       |      $$    $$/ $$    $$ |      $$    $$/ $$    $$ |$$ |  $$ |______ $$ |    $$ |      
$$/      $$/  $$$$$$$/  $$$$$$$/  $$$$$$$/       $$$$$$$/   $$$$$$$ |      $$$$$$$/   $$$$$$$/ $$/   $$//      |$$/     $$/       
                                                           /  \__$$ |                                   $$$$$$/                   
                                                           $$    $$/                                                              
                                                            $$$$$$/                                                               
"""


def create_user_model(apps,project_name):

    base_models_file = f"""from django.db import models
import uuid
from django.contrib.auth.hashers import make_password

class {project_name}User(models.Model):
    email = models.EmailField()
    name = models.TextField(max_length=100, blank=True, null=True)
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.TextField(max_length=100)

    def set_password(self, password):
        new_password = make_password(password)
        return new_password

    """

    base_serializers_file = f"""from rest_framework import serializers
from ..models import base_models


class {project_name}UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = base_models.{project_name}User
        fields = '__all__'
        
"""

    base_views_file = """
from rest_framework.views import APIView
from ..models import base_models
from ..serializers import base_serializers
from rest_framework.response import Response
import uuid
from django.contrib.auth.hashers import check_password
    
class Login(APIView):

    #check if the user is logged in from the token

    def get(self, request):

        headers = request.headers

        try:
            token = headers['token']
            assert token != None
            assert uuid.UUID(token)
            assert base_models.{project_name}User.objects.filter(token=token).exists()
        except:
            return Response({'success': False, 'message': "No token provided or invalid token"}, status=200)


        serialized_user = base_serializers.{project_name}UserSerializer(base_models.{project_name}User.objects.get(token=token))

        return Response({'success': True, 'user': serialized_user.data}, status=200)


class LoginWithEmail(APIView):

        #log in the user with email and password

        def get(self, request):

            headers = request.headers

            try:
                email = headers['email'].lower()
                password = headers['password']
                assert email != None
                assert password != None
                assert base_models.{project_name}User.objects.filter(email=email).exists()
                user = base_models.{project_name}User.objects.get(email=email)
                user_password_hash = user.password
                assert check_password(password, user_password_hash)
            except:
                return Response({'success': False, 'message': 'Invalid email or password'}, status=200)

            return Response({'success': True, 'message': 'User logged in successfully', 'user': base_serializers.{project_name}UserSerializer(user).data}, status=200)
""".replace("{project_name}",project_name)


    for app in apps:
        open(f"{app}/models/base_models.py", "w",encoding="utf-8").write(base_models_file)
        open(f"{app}/serializers/base_serializers.py", "w",encoding="utf-8").write(base_serializers_file)
        open(f"{app}/views/base_views.py", "w",encoding="utf-8").write(base_views_file)
        open(f"{app}/urls.py", "w",encoding="utf-8").write(f"from django.urls import path\nfrom .views.base_views import *\n\nurlpatterns = [\n    path('login/', Login.as_view()),\n    path('login_with_email/', LoginWithEmail.as_view()),\n\n]")
        open(f"{app}/admin.py", "w",encoding="utf-8").write(f"from django.contrib import admin\nfrom .models.base_models import *\n\nadmin.site.register({project_name}User)")


def create_runner():
    runner_file = """import os

def get_ip():
    # if you want to host on your local network
    # ip = str(subprocess.check_output("ipconfig")).split("Adresse IPv4. . . . . . . . . . . . . .: ")[2].split("\\r")[0]
    
    ip = "127.0.0.1"
    return ip

ip = get_ip()
print("hosting on",ip)

lines = [
    'python manage.py makemigrations',
    'python manage.py migrate --run-syncdb',
    f'python manage.py runserver {ip}:8000'
]

for line in lines:
    os.system(line)"""

    open(f"runner.py", "w",encoding="utf-8").write(runner_file)

