from django.contrib import admin

from petitions.models import Petition, Signature, Suggestion


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    fields = ('title', 'body')
    list_display = ('title', 'body')


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
make_active.short_description = "Confirm selected signatures"


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    fields = ('name', 'job_title', 'affiliation', 'petition', 'active', 'initial',
            'timestamp')
    list_display = ('name', 'job_title', 'affiliation', 'petition', 'active', 'initial',
            'timestamp')
    list_filter = ('active', 'initial')
    search_fields = ['name', 'job_title', 'affiliation', 'email']
    actions = [make_active]


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    fields = ('name', 'job_title', 'affiliation', 'petition', 'suggestion', 'timestamp')
    list_display = ('name', 'job_title', 'affiliation', 'petition', 'suggestion', 'timestamp')
    search_fields = ['name', 'job_title', 'affiliation', 'suggestion']


admin.site.site_title = 'WEDF Open Letter Backend'
admin.site.site_header = 'WEDF Open Letter Backend'
admin.site.site_url = None
