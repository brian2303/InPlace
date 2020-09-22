from django.forms import *
from apps.usuarios.models import User

class UserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image',
        labels = {
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'email':'Correo',
            'username':'Usuario',
            'password':'Contraseña',
            'image':'Imagen'
        }
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese Nombre(s)',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese Apellido(s)',
                }
            ),            
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su Usuario',
                }
            ),            
            'password': PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese su Contraseña',
                }
            ),       
        }
        exclude = ['groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data