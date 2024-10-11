from django import forms
from .models import Item,Categoria, Usuario

class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Ingrese su correo electrónico",
        "class": "form-control",
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Ingrese su contraseña",
        "class": "form-control",
    }))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Correo"
        self.fields['password'].label = "Contraseña"

class EditarPerfilForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('email','nombre','direccion','edad','phone_number')

class RegistroForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('email','nombre','password')

        widgets = {
            'email':forms.TextInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
            'nombre':forms.TextInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
            'password':forms.PasswordInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo"
        self.fields['password'].label = "Contraseña"

class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre',)
        
        widgets = {
            'nombre':forms.TextInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
        }

class ItemForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Item
        fields = ('nombre','stock','precio','descuento','descripcion','categoria','imagen')

        widgets = {
            'nombre':forms.TextInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
            'stock':forms.NumberInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
            'precio':forms.NumberInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
            'descuento':forms.NumberInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
            'descripcion':forms.Textarea(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
            'imagen':forms.FileInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
        }


