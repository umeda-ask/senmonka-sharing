from django import forms
from django.contrib.auth.models import User
from .models import Account

# フォームクラス作成
class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email','password')
        # フィールド名指定
        labels = {'username':"ユーザーID",'email':"メール"}

class AddAccountForm(forms.ModelForm):
    class Meta():
        # モデルクラスを指定
        model = Account
        fields = ('last_name','first_name','account_image',)
        labels = {'last_name':"苗字",'first_name':"名前",'account_image':"写真アップロード",}

class SodanForm(forms.Form):
    companyname = forms.CharField(
        label='companyname',
        max_length=100,
        required=True,
        help_text='必須',
    )
    name = forms.CharField(
        label='customername',
        max_length=100,
        required=True,
        help_text='必須',
    )
    phone = forms.CharField(
        label='phone',
        max_length=100,
        required=True,
        help_text='必須',
    )
    mail = forms.CharField(
        label='mail',
        max_length=100,
        required=True,
        help_text='必須',
    )
    genre = forms.CharField(
        label='genre',
        max_length=100,
        required=True,
        help_text='必須',
    )
    consultation = forms.CharField(
        label='consultation',
        max_length=100,
        required=True,
        help_text='必須',
    )