from django.urls import path
from . import views
from apps.usuarios.views import *
from .views.usuarios.views import *
from .views.roles.views import *

urlpatterns = [
    # path('', views.index_usuarios),
    path('lista', UserListView.as_view(), name='usuarios_lista'),
    path('crear', UserCreateView.as_view(), name='usuario_crear'),
    path('editar<int:pk>/', UserUpdateView.as_view(), name='usuario_editar'),
    path('eliminar<int:pk>/', UserDeleteView.as_view(), name='usuario_eliminar'),
    path('change/group/<int:pk>/', UserChangeGroup.as_view(), name='user_change_group'),
    # roles
    path('rol/lista', RolListView.as_view(), name='roles_lista'),

]