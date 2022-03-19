from django.urls import path
from legal_map.legal_help import views


urlpatterns = (
    path('', views.legal_index_view, name='legal index'),
    path('create/', views.create, name='company create'),
    path('companies/details/<int:pk>', views.company_details, name='company details'),
    path('companies/mycompanies/', views.list_my_companies, name='list my companies'),
    path('companies/edit/<int:pk>', views.edit_company, name='company edit'),
    path('companies/delete/<int:pk>', views.delete_company, name='company delete'),
    path('find/<int:pk>', views.find_companies, name='find companies'),
)