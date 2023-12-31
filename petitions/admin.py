from django.contrib import admin

from petitions.models import Petition, Signature, Suggestion


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    fields = ('title', 'body')
    list_display = ('title', 'body')


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
make_active.short_description = "Confirm selected signatures"


def make_non_initial(modeladmin, request, queryset):
    queryset.update(initial=False)
make_non_initial.short_description = "Move selected signatures to non-initial"


def make_initial(modeladmin, request, queryset):
    queryset.update(initial=True)
make_initial.short_description = "Move selected signatures to initial"


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    fields = ('name', 'job_title', 'affiliation', 'petition', 'active', 'initial',
            'order', 'timestamp')
    list_display = ('name', 'job_title', 'affiliation', 'petition', 'active', 'initial',
            'order', 'timestamp')
    list_filter = ('active', 'initial')
    search_fields = ['name', 'job_title', 'affiliation', 'email']
    actions = [make_active, make_initial, make_non_initial]


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    fields = ('name', 'job_title', 'affiliation', 'email', 'petition', 'suggestion', 'timestamp')
    list_display = ('name', 'job_title', 'affiliation', 'email', 'petition', 'suggestion', 'timestamp')
    search_fields = ['name', 'job_title', 'affiliation', 'email', 'suggestion']


admin.site.site_title = 'WEDF Open Letter Backend'
admin.site.site_header = 'WEDF Open Letter Backend'
admin.site.site_url = None
