"""Class for adjust admin web-page."""

from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    """Class for adjust the choice in admin page."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Class for adjust the question in admin page."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'end_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
