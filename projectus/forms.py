from django import forms
from .models import Comment, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': ''}
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Escreva seu comentário...',
            })
        }


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        label='E-mail',
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Este e-mail já está cadastrado.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        users = User.objects.filter(
            email__iexact=email
        ).exclude(pk=self.instance.pk)

        if users.exists():
            raise forms.ValidationError(
                'Este e-mail já está cadastrado.'
            )

        return email
    
    
class PostForm(forms.ModelForm):
    # Formulário para criar e editar publicações.

    class Meta:
        model = Post  # Usa o modelo Post já existente.

        fields = [
            'title',      # Título da publicação.
            'summary',    # Resumo do artigo.
            'thumbnail',  # URL da imagem de capa.
            'textbody',   # Conteúdo completo do artigo.
        ]

        labels = {
            'title': 'Título',
            'summary': 'Resumo',
            'thumbnail': 'URL da imagem de capa',
            'textbody': 'Conteúdo da publicação',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título da publicação',
            }),

            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escreva um breve resumo',
            }),

            'thumbnail': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com/imagem.jpg',
            }),

            'textbody': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': 'Escreva o conteúdo completo do artigo',
            }),
        }
