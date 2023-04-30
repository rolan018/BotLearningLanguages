from django.contrib import admin
from .models import Profile
from .models import ActionWord
from .models import ActionMaterial
from .models import ActionLesson
from .forms import ProfileForm
from .forms import ActionWordForm
from .forms import ActionLessonForm
from .forms import ActionMaterialForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'name', 'telephone', 'email')
    form = ProfileForm


@admin.register(ActionWord)
class ActionWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'text', 'created_at')
    form = ActionWordForm


@admin.register(ActionMaterial)
class ActionMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'topic', 'url', 'mark',  'created_at')
    form = ActionMaterialForm


@admin.register(ActionLesson)
class ActionLessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'date', 'topic', 'mark', 'created_at')
    form = ActionLessonForm
