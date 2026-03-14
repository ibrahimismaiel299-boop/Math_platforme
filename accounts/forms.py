from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pages.models import Profile

class StudentSignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, label="رقم الواتساب (مهم للتفعيل)")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone_number',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # إنشاء البروفايل وربطه بالرقم المدخل
            Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user
