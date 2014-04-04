from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mycv.apps.projects.models import Skill
from mycv.apps.accounts.models import MyCVUser


class SkillsInline(admin.StackedInline):
    model = Skill


class MyCVUserAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('User Info'), {
            'classes': ('grp-collapse grp-open', 'wide',),
            'fields': ('first_name', 'last_name', 'email', )
        }),
        #(_('Address'), {
        #    'classes': ('grp-collapse grp-closed',),
        #    'fields': (
        #        'city',
        #        'zip_code',
        #    )
        #}),
        (_('User Info Misc'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('avatar', 'github_username',)
        }),
        (_('Permissions'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('is_active', )
        }),
        (_('Important dates'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('last_login', 'date_joined')
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    inlines = [SkillsInline, ]
    #change_list_template = "admin/change_list_filter_sidebar.html"
    #actions = ['']
    readonly_fields = (
        'last_login',
        'date_joined',
    )
    list_display = ('first_name', 'last_name', 'email', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined',)

    class Meta:
        model = MyCVUser

admin.site.register(MyCVUser, MyCVUserAdmin)
