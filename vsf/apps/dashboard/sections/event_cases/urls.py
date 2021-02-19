from django.conf.urls import include
from django.urls import path
from . import views
app_name = 'event_cases'

urlpatterns = [
    path(
        '',
        views.CasesListView.as_view(),
        name="list_cases"
    ),  
]