"""localgag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
# from rest_framework_jwt.views import obtain_jwt_token as login
from localgag.views.account import login, verify, send_code
from localgag.views.file_upload import upload_file
from localgag.views.user import create_user, get_users, get_user, delete_user, update_user_location
from localgag.views.comment import update_comment
from localgag.views.reply import delete_reply, reply_to_reply
from localgag.views.status import create_status, delete_status, get_status, get_statuses, reply_to_status
from localgag.helpers.method_splitter import method_splitter


urlpatterns = [
    url(r'^admin', admin.site.urls), # admin, DBrocks23

    url(r'^login', login),
    url(r'^verify', verify),
    url(r'^code', send_code),

    url(r'^upload/(?P<filename>[^/]+)$', upload_file),

    url(r'^users/(?P<user_id>[0-9a-f-]+)/location', update_user_location),
    url(r'^users/(?P<user_id>[0-9a-f-]+)', method_splitter, {'GET': get_user, 'POST': delete_user}),
    url(r'^users', csrf_exempt(method_splitter), {'GET': get_users, 'POST': create_user}),

    url(r'^statuses/(?P<status_id>[0-9a-f-]+)/reply', reply_to_status),
    url(r'^statuses/(?P<status_id>[0-9a-f-]+)', method_splitter, {'GET': get_status, 'DELETE': delete_status}),
    url(r'^statuses', method_splitter, {'GET': get_statuses, 'POST': create_status}),

    url(r'^comments/(?P<comment_id>[0-9a-f-]+)', update_comment),

    url(r'^replies/(?P<reply_id>[0-9a-f-]+)/reply', reply_to_reply),
    url(r'^replies/(?P<reply_id>[0-9a-f-]+)', delete_reply),
]

"""
URL Conventions:
POST http://localhost:8000/login - login

POST http://localhost:8000/users - create user
GET http://localhost:8000/users - get users
GET http://localhost:8000/users/{user_id} - get user
DELETE http://localhost:8000/users/{user_id} - delete user
POST http://localhost:8000/users/{user_id}/location - update user location

POST http://localhost:8000/statuses - create status
GET http://localhost:8000/statuses - get statuses
GET http://localhost:8000/statuses/{status_id} - get status
DELETE http://localhost:8000/statuses/{status_id} - delete status
POST http://localhost:8000/statuses/{status_id}/reply - reply to status

POST http://localhost:8000/comments/{comment_id} - update comment (message or vote)

POST http://localhost:8000/replies/{reply_id}/reply - reply to reply
POST http://localhost:8000/replies/{reply_id} - delete reply

"""