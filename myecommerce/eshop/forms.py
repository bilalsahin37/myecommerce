from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Order,CustomUser,Product,Category




class OrderForm(forms.ModelForm):
    class  Meta:
        model=Order
        fields= ['full_name','email','address']
        widget={
        'full_name': forms.TextInput(attrs={'class':'form-control'}),
        'email': forms.EmailInput(attrs={'class':'form-control'}),
        'address': forms.Textarea(attrs={'class':'form-control'}),
        }

    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if Order.objects.filter(email=email,paid=False).exists():
            raise forms.ValidationError("You have an unpaid order with this email address.")
        return email






class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields=('username','password1','password2')
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")




        
                
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('username','email','bio','location')
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return 






class CustomAuthenticationForm(AuthenticationForm):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'autofocus':True}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput)






class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ['name','price','stock','category','description','available','image']
        widgets ={
            'description':forms.Textarea(attrs={'rows':4,'class':'form-control'}),
            'image':forms.ClearableFileInput(attrs={'rows':4,'class':'form-control-file'}),
        }







class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','description'] 
        widgets = {
            'description':forms.Textarea(attrs={'rows':4,'class':'form-control'})
        }