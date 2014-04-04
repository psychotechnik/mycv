from django.views.generic.list import ListView
from mycv.apps.projects.models import Project, Client, ClientObjective
from mycv.apps.accounts.models import MyCVUser


class ClientListView(ListView):
    model = Client
    template_name = "resume.html"

    def get_queryset(self):
        return Client.objects.exclude(is_draft=True)

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        applicant = MyCVUser.objects.get(email='pk@slipperyslo.pe')
        context.update({
            'applicant': applicant,
        })
        return context

client_list_view = ClientListView.as_view()


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    queryset = Project.objects.exclude(is_draft=True)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context.update({
            # 'instance_archived_list':
        })
        print context
        return context

project_list_view = ProjectListView.as_view()