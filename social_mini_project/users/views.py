from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy

from .forms import EditingProfileForm, RegistrationProfileForm
from .models import CustomUser


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegistrationProfileForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("posts:post_list")


class ProfileView(DetailView):
    model = CustomUser
    template_name = "users/profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditingProfileForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("posts:post_list")

    def get_object(self, queryset=None):
        # Редактирование только своего профиля
        return self.request.user


class ProfileListView(ListView):
    model = CustomUser
    template_name = "users/profile_list.html"
    context_object_name = "profiles"
    paginate_by = 10  # Пагинация оп 10 пользователей на странице
