from django import forms
from django.forms import fields, widgets
from .models import Comments, Post, NewsPaper, Payment
from django.contrib.auth.models import User,Permission


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        


class ResetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password', 'new_password', 'confirm_password')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'subject', 'images', 'video')


class ParentForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model=Comments
#         fields=('post','comments')


class PaymentRegister(forms.ModelForm):
    user = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "User"}))
    invoiceid = forms.IntegerField(widget=forms.TextInput(
        attrs={"placeholder": "Invoice number"}))
    name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Name from the invoice"}))
    clientid = forms.IntegerField(widget=forms.TextInput(
        attrs={"placeholder": "Clientid from the invoice"}))
    amount = forms.DecimalField(widget=forms.TextInput(
        attrs={"placeholder": "Total amount to pay"}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"placeholder": "example@email.com"}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Phone number"}))

    class Meta:
        model = Payment
        fields = ['invoiceid', 'user', 'name',
                  'clientid', 'amount', 'email', 'phone']

    def save(self, commit=True):
        payment = super(PaymentRegister, self).save(commit=False)
        payment.user = self.cleaned_data['user']
        payment.invoiceid = self.cleaned_data['invoiceid']
        payment.name = self.cleaned_data['name']
        payment.clientid = self.cleaned_data['clientid']
        payment.amount = self.cleaned_data['amount']
        payment.email = self.cleaned_data['email']
        payment.phone = self.cleaned_data['phone']
        if commit:
            payment.save()
        return payment
