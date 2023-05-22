from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.accountRegistration.as_view(), name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_, name='login'),
    path('todolist/', views.todolist_, name='todolist'),
    path('search/', views.search_, name='search'),
    path('search_keyword/', views.search_keyword_, name='search_keyword'),
    path('contact/', views.contact_, name='contact'),
    path('contact_conf/', views.contact_conf_, name='contact_conf'),
    path('contact_comp/', views.contact_comp_, name='contact_comp'),
    path('select_month/', views.select_month_, name='select_month'),
    path('case_detail/', views.case_detail_, name='case_detail'),
    path('case_genre/', views.case_genre_, name='case_genre'),
    path('todo_detail/', views.todo_detail_, name='todo_detail'),
]