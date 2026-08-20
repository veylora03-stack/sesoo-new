import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Lead

class LeadForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label='')
    source_page = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Lead
        fields = ['full_name', 'phone', 'email', 'service_type', 'budget', 'message', 'consent', 'source_page']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'نام و نام خانوادگی'}),
            'phone': forms.TextInput(attrs={'class': 'input', 'placeholder': 'شماره تماس'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'ایمیل (اختیاری)'}),
            'service_type': forms.Select(attrs={'class': 'select'}),
            'budget': forms.Select(attrs={'class': 'select'}),
            'message': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'پیام شما', 'rows': 4}),
            'consent': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['consent'].required = True

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        phone = re.sub(r'[\s\-\(\)a-zA-Z]', '', phone)
        
        if phone.startswith('00989'):
            phone = '09' + phone[5:]
        elif phone.startswith('989'):
            phone = '09' + phone[3:]
        elif phone.startswith('9') and len(phone) == 10:
            phone = '0' + phone
            
        mobile_pattern = r'^09\d{9}$'
        landline_pattern = r'^0\d{2,3}\d{7,8}$'
        
        if not (re.match(mobile_pattern, phone) or re.match(landline_pattern, phone)):
            raise ValidationError("شماره تماس معتبر نیست. لطفاً شماره تماس خود را با فرمت صحیح وارد کنید.")
            
        return phone

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '').strip()
        if len(name) < 3:
            raise ValidationError("لطفاً نام و نام خانوادگی را کامل وارد کنید.")
        return name