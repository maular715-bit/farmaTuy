from django.urls import path
from . import views_ui as views

urlpatterns = [
    path('', views.FarmaciaListView.as_view(), name='home'),

    # Farmacia
    path('farmacias/', views.FarmaciaListView.as_view(), name='farmacia_list'),
    path('farmacias/create/', views.FarmaciaCreateView.as_view(), name='farmacia_create'),
    path('farmacias/<uuid:pk>/', views.FarmaciaDetailView.as_view(), name='farmacia_detail'),
    path('farmacias/<uuid:pk>/edit/', views.FarmaciaUpdateView.as_view(), name='farmacia_edit'),
    path('farmacias/<uuid:pk>/delete/', views.FarmaciaDeleteView.as_view(), name='farmacia_delete'),

    # Medicamento
    path('medicamentos/', views.MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamentos/create/', views.MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamentos/<uuid:pk>/', views.MedicamentoDetailView.as_view(), name='medicamento_detail'),
    path('medicamentos/<uuid:pk>/edit/', views.MedicamentoUpdateView.as_view(), name='medicamento_edit'),
    path('medicamentos/<uuid:pk>/delete/', views.MedicamentoDeleteView.as_view(), name='medicamento_delete'),

    # Inventario
    path('inventario/', views.InventarioListView.as_view(), name='inventario_list'),
    path('inventario/create/', views.InventarioCreateView.as_view(), name='inventario_create'),
    path('inventario/<int:pk>/edit/', views.InventarioUpdateView.as_view(), name='inventario_edit'),
    path('inventario/<int:pk>/delete/', views.InventarioDeleteView.as_view(), name='inventario_delete'),

    # Tipos
    path('tipos/', views.TipoListView.as_view(), name='tipo_list'),
    path('tipos/create/', views.TipoCreateView.as_view(), name='tipo_create'),
    path('tipos/<uuid:pk>/edit/', views.TipoUpdateView.as_view(), name='tipo_edit'),
    path('tipos/<uuid:pk>/delete/', views.TipoDeleteView.as_view(), name='tipo_delete'),

    # Usuarios
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/create/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<uuid:pk>/edit/', views.UsuarioUpdateView.as_view(), name='usuario_edit'),
    path('usuarios/<uuid:pk>/delete/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
    path('public/', views.PublicSearchView.as_view(), name='public_search'),
]
