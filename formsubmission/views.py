from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import UserProfileForm


class UserListView(LoginRequiredMixin, ListView):
    """
    View class to display a list of user profiles.
    """

    model = UserProfile
    template_name = "formsubmission/user_list.html"
    context_object_name = "users"
    login_url = "/login/"

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = UserProfile.objects.all()
        else:
            queryset = UserProfile.objects.filter(is_deleted=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_user"] = self.request.user
        return context


class UserDetailView(DetailView):
    """
    View class to display the details of a user profile.
    """

    model = UserProfile
    template_name = "formsubmission/user_detail.html"
    context_object_name = "user"


class UserCreateView(CreateView):
    """
    View class to create a new user profile.
    """

    model = UserProfile
    form_class = UserProfileForm
    template_name = "formsubmission/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(self.request, "User profile created successfully.")
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """
    View class to update an existing user profile.
    """

    model = UserProfile
    form_class = UserProfileForm
    template_name = "formsubmission/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(self.request, "User profile updated successfully.")
        return super().form_valid(form)


class UserDeleteView(View):
    """
    View class to mark a user profile as deleted (soft delete).
    """

    model = UserProfile
    template_name = "formsubmission/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        return render(request, self.template_name, {"user": user_profile})

    def post(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user_profile.is_deleted = True
        user_profile.deleted_at = timezone.now()
        user_profile.save()
        messages.success(request, "User profile marked as deleted.")

        return redirect(self.success_url)


class UserUndeleteView(View):
    template_name = "formsubmission/user_confirm_undelete.html"

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(pk=self.kwargs["pk"])
        return render(request, self.template_name, {"user": user_profile})

    def post(self, request, *args, **kwargs):
        # Retrieve the user profile object to undelete
        user_profile = get_object_or_404(UserProfile, id=self.kwargs["pk"])

        # Check if the user profile is marked as deleted
        if user_profile.is_deleted:
            # Undelete the user profile
            user_profile.is_deleted = False
            user_profile.save()
            messages.success(request, "User profile undeleted successfully.")

        # Redirect to the User Profiles page
        return redirect("user_list")
