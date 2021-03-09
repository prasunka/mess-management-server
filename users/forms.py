from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class NewUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)
