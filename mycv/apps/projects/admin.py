from django.contrib import admin

from mycv.apps.projects.models import (
    Project,
    ProjectFeature,
    StackItem,
    Client,
    ClientObjective,
    Skill,
)


class ClientObjectiveInline(admin.StackedInline):
    model = ClientObjective


class ProjectFeatureInline(admin.StackedInline):
    model = ProjectFeature
    fields = ('name', )
    #readonly_fields = ('date_added',)
    extra = 3
    #raw_id_fields = ('location',)
    #autocomplete_lookup_fields = { 'fk': ['location'], }
    #ordering = ('date_added',)


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

    inlines = [ProjectFeatureInline,]

    # define the raw_id_fields
    raw_id_fields = ('stack_items',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        #'fk': [''],
        'm2m': ['stack_items', ],
    }
admin.site.register(Project, ProjectsAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_index', 'is_draft')
    search_fields = ('name', )
    inlines = [ClientObjectiveInline, ]
admin.site.register(Client, ClientAdmin)


class ClientObjectiveAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )
admin.site.register(ClientObjective, ClientObjectiveAdmin)


class ProjectFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
admin.site.register(ProjectFeature, ProjectFeatureAdmin)


class StackItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
admin.site.register(StackItem, StackItemAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('description', 'category')
    list_filter = ('category', )
    search_fields = ('description',)
admin.site.register(Skill, SkillAdmin)
