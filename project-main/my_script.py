# my_script.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liveblog_project.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
print(User.objects.all())
