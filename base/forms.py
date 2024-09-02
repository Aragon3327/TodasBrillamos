from django import forms
from .models import Item,Categorias

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

class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ('nombre',)
        
        widgets = {
            'nombre':forms.TextInput(attrs={
                'autocomplete':'off',
                'class' : 'form-control mb-2'
            }),
        }

class ItemForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categorias.objects.all(),
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


