from django import forms
from . import models
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
        help_text=''
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.usuario = usuario 



    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password2','password', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}


        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')


        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()


        error_msg_user_exist = 'Usuario já existe!'
        error_msg_email_exist = 'E-mail já registrado!'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatiorio.'

#usuarios logados
        if self.usuario:
            if usuario_data != usuario_db.username:
                if usuario_db:
                    validation_error_msgs['username'] = error_msg_user_exist


            if email_data != email_db.email:
                if email_db:
                    validation_error_msgs['email'] = error_msg_email_exist


            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password_data) <6:
                    validation_error_msgs['password'] = error_msg_password_short

#usuarios não logas = cadastro
        else:
            print(usuario_db, usuario_data)
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exist


            if email_db:
                validation_error_msgs['email'] = error_msg_email_exist

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            if not password2_data:
                    validation_error_msgs['password2'] = error_msg_required_field

            if password_data != password2_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

            if len(password_data) <6:
                validation_error_msgs['password'] = error_msg_password_short


        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))