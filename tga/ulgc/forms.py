from django import forms
from .models import Profile
from .models import ActionWord
from .models import ActionLesson
from .models import ActionMaterial


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'telegram_id',
            'name',
            'telephone',
            'email',
        )
        widgets = {
            'telegram_id': forms.TextInput,
            'name': forms.TextInput,
            'telephone': forms.TextInput,
            'email': forms.TextInput,
        }


class ActionWordForm(forms.ModelForm):

    class Meta:
        model = ActionWord
        fields = (
            'text',
        )
        widgets = {
            'text': forms.TextInput,
        }


class ActionLessonForm(forms.ModelForm):

    class Meta:
        model = ActionLesson
        fields = (
            'date',
            'topic',
            'mark',
        )
        widgets = {
            'date': forms.TextInput,
            'topic': forms.TextInput,
            'mark': forms.NumberInput,
        }


class ActionMaterialForm(forms.ModelForm):

    class Meta:
        model = ActionMaterial
        fields = (
            'topic',
            'url',
            'mark',
        )
        widgets = {
            'topic': forms.TextInput,
            'url': forms.TextInput,
            'mark': forms.NumberInput,
        }
