import os

from selenium import webdriver

SELENIUM_WEBDRIVERS = {
    "default": {"callable": webdriver.Chrome, "args": (), "kwargs": {}},
    "firefox": {"callable": webdriver.Firefox, "args": (), "kwargs": {}},
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',	
        'NAME': 'boarddb',	
        'USER': 'board',	
        'PASSWORD': 'board',	
        'HOST': 'localhost',	
        'PORT': '5432',	
    }	
}
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "portal.context_processors.process_newsletter_form",
            ]
        },
    }
]

if os.environ.get("SELENIUM_HEADLESS", None):
    from pyvirtualdisplay import Display

    display = Display(visible=0, size=(1624, 1024))
    display.start()
    import atexit

    atexit.register(lambda: display.stop())

INSTALLED_APPS = ["portal"]
PIPELINE_ENABLED = False
ROOT_URLCONF = "example_project.example_project.urls"
STATIC_ROOT = "example_project/example_project/static"
SECRET_KEY = "bad_test_secret"

DOTMAILER_URL = "https://test/"
DOTMAILER_USER = "help.tryonboard@gmail.com"
DOTMAILER_PASSWORD = "AcmeBoard099"
DOTMAILER_DEFAULT_PREFERENCES = [{"trout": True}]

from django_autoconfig.autoconfig import configure_settings

configure_settings(globals())