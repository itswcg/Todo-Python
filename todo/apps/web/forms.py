from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm


class SignInForm(AuthenticationForm):
    captcha = CaptchaField(label='验证码')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30,
                               required=True,
                               label='用户名')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}),
                            max_length=50,
                            required=True,
                            label='邮箱')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='密码',
                               required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label='确认密码',
                                       required=True)
    captcha = CaptchaField(label='验证码')

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'captcha']

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(['密码不匹配'])
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    # sex = forms.CharField(max_length=1, widget=forms.Select(choices=(
    #     ('B', 'Boy'),
    #     ('G', 'Girl'),
    # )))

    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                   label='旧密码', required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                   label='新密码', required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label='确认新密码', required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ProfileForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        user_id = self.cleaned_data.get('id')
        user = User.objects.get(pk=user_id)

        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(['密码错误'])

        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class(['密码不一致'])

        return self.cleaned_data
