"""
Django settings for Chunju project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9@pnpjugxy&q*yu#lb#0$+0&c3l@!da+41c_=jkohr6%()jtr&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webcore.apps.WebcoreConfig',
    'companysafe.apps.CompanysafeConfig',
    'webapp.apps.WebappConfig',
    'web.apps.WebConfig',
    'rbac.apps.RbacConfig',
    'stark.apps.StarkConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'rbac.middlewares.rbac.RbacMiddleware',
]

ROOT_URLCONF = 'Chunju.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Chunju.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chunju',  # 数据库名字
        'USER': 'postgres',  # 登录用户名
        'PASSWORD': 'mark8872',
        'HOST': '127.0.0.1',  # 数据库IP地址
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'media'),
    # os.path.join(os.path.dirname(__file__), '../static/').replace('\\', '/'),
)
# 文件上传的路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# wechat 企业微信设置
APP_NAME = '春菊电器'

CORP_ID = 'ww70cbd82f459f1fa4'  # 企业ID
APP_ID = '1000014'  # 应用ID
APP_SECRET = '6A_tji_mYLVESw9-JOaAJ2tSCOr90t8Vdu_hD1m2d1g'  # 应用Secret
TOKEN_1000014 = "sw39NoFIB9xPbDaWeHSfw"  # 应用的 接收消息服务器的Token
ENCODING_AES_KEY_1000014 = '7AhkxywwptXvxKCcyIEX4B57cwH4c5pOe0OYkihQJPd'  # 应用的 接收消息服务器的EncodingAESKey

DATA_UPLOAD_MAX_MEMORY_SIZE = 15242880  # 设置上传文件的大小 默认设置为5M

#  ###################权限相关的配置#####################
PERMISSION_SESSION_KEY = 'chunju_permission_url_list'

MENU_SESSION_KEY = 'chunju_menu_list'

# url白名单 不做权限验证
VALID_URL_LIST = [
    ':webcore_login',  # 登陆
    "webcore:webcore_login",
    'webcore:webcore_logout',  # 注销
    'webapp:webcore_error',  # 错误
    'webapp:webapp_entwxlogin',  # 企业微信登陆
    '/admin/.*',  # 后台管理
    '/media/.*',  # 媒体文件
    'webapp:WW_verify_83z6GYOPGCfBqcDy',  # 企业微信验证文件
    'webapp:webapp_content',  # 企业微信消息
    'webapp:webapp_oauth_user',  # 企业微信 网页登陆认证
]

X_FRAME_OPTIONS = 'ALLOWALL'  # 充许 iform访问

#  自动发现项目中URL--排除不自动发现的URL
AUTO_DISCOVER_EXCLUDE = [
    '/admin/.*',
]
