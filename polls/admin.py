from django.contrib import admin

from . import models
# Register your models here.


class ChoiceInline(admin.StackedInline):
    model = models.Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ["creation_date", 'question_text']
    inlines = [ChoiceInline]


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Choice)
