from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class GenStatView(TemplateView):
    template_name = "users/index.html"
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # context["ad"] = Ad.objects.all()
        return self.render_to_response(context)