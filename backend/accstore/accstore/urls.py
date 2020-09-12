from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('<str:lang>/', include('accstore_app.urls'))
]
