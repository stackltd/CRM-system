from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, reverse
from django.views.generic import DeleteView, CreateView, UpdateView


class CustomCreateView(CreateView):
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save(commit=False)
        resp = super().form_valid(form)
        return resp


class CustomDeleteView(DeleteView):
    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            messages.error(
                request,
                f"Нельзя удалить запись! Связанные записи: {e.protected_objects}",
            )
            model_name = self.model._meta.verbose_name_plural
            return redirect(f"/{model_name}")


class CustomUpdateView(UpdateView):
    def get_success_url(self):
        model_name = self.model._meta.verbose_name_plural
        url = reverse(
            f"{model_name}:{model_name[:-1]}-detail", kwargs={"pk": self.object.pk}
        )
        return url


class PermissionsMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm(self.permission_required)

    def handle_no_permission(self):
        referer = self.request.META.get('HTTP_REFERER') or "/"
        messages.warning(
            self.request,
            "Ошибка. У вас нет прав на выполнение данного действия"
        )
        return redirect(referer)