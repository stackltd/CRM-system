from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Lead
from ads.models import Ad


class LeadsListView(ListView):    
    template_name = "leads/leads-list.html"
    context_object_name = "leads"
    queryset = Lead.objects.select_related("ad")


class LeadCreateView(CreateView):
    model = Lead
    fields = ["ad", "first_name", "last_name", "email", "phone"]
    template_name = "leads/leads-create.html"
    success_url = reverse_lazy("leads:leads-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save(commit=False)
        resp = super().form_valid(form)
        return resp


class LeadDeleteView(DeleteView):
    model = Lead
    template_name = "leads/leads-delete.html"
    success_url = reverse_lazy("leads:leads-list")


class LeadDetailView(DetailView):    
    template_name = "leads/leads-detail.html" # удалить, если имя шаблона в формате 'model_detail.html'
    queryset = Lead.objects.select_related("ad")


class LeadUpdateView(UpdateView):
    model = Lead
    fields = ["ad", "first_name", "last_name", "email", "phone"]
    template_name = "leads/leads-edit.html"

    def get_success_url(self): # получаем ссылку на детализацию объекта, который был изменен и на который переходим после отправки формы изменения
        url = reverse("leads:lead-detail", kwargs={"pk": self.object.pk})
        return url
