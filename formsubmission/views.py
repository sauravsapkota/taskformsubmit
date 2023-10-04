from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from taskformsubmit.settings import LOGIN_URL, PAGINATED_BY
from .forms import UserProfileForm
from .models import UserProfile


class UserListView(LoginRequiredMixin, ListView):
    """
    View class to display a list of user profiles.
    """

    model = UserProfile
    template_name = "formsubmission/user_list.html"
    context_object_name = "users"
    paginate_by = PAGINATED_BY
    login_url = reverse_lazy(LOGIN_URL)

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = UserProfile.objects.get_all_profiles()
        else:
            queryset = UserProfile.objects.get_active_profiles()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        self.queryset = self.get_queryset()
        paginator = Paginator(self.queryset, self.paginate_by)

        try:
            page = paginator.page(self.request.GET.get("page", 1))
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context["page_obj"] = page
        return context


class UserDetailView(DetailView):
    """
    View class to display the details of a user profile.
    """

    model = UserProfile
    template_name = "formsubmission/user_detail.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        try:
            user = self.get_queryset().get(pk=self.kwargs.get('pk'))
            if not self.request.user.is_superuser and user.is_deleted:
                raise Http404("User profile does not exist.")
            return user
        except Exception:
            raise Http404("User profile does not exist.")


class UserCreateView(CreateView):
    """
    View class to create a new user profile.
    """

    model = UserProfile
    form_class = UserProfileForm
    template_name = "formsubmission/user_form.html"

    def get_success_url(self):
        messages.success(self.request, "User profile created successfully.")
        return reverse("user_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form submission. Please check your input.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class UserUpdateView(UpdateView):
    """
    View class to update an existing user profile.
    """

    model = UserProfile
    form_class = UserProfileForm
    template_name = "formsubmission/user_form.html"

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "User profile updated successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Form submission failed. Please check the form for errors.")
        return self.render_to_response(self.get_context_data(form=form))


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
        try:
            user_profile = self.get_object()
            user_profile.mark_as_deleted()
            messages.success(request, "User profile marked as deleted.")
        except Exception as e:
            messages.error(request, str(e))
        return redirect(self.success_url)


class UserUndeleteView(View):
    template_name = "formsubmission/user_confirm_undelete.html"

    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, pk=self.kwargs["pk"])
        return render(request, self.template_name, {"user": user_profile})

    def post(self, request, *args, **kwargs):
        # Retrieve the user profile object to undelete
        user_profile = get_object_or_404(UserProfile, id=self.kwargs["pk"])

        # Check if the user profile is marked as deleted
        if user_profile.is_deleted:
            # Undelete the user profile
            user_profile.is_deleted = False
            user_profile.save(update_fields=['is_deleted'])
            if not user_profile.is_deleted:
                messages.success(request, "User profile undeleted successfully.")
            else:
                messages.error(request, "User profile does not exist.")

        # Redirect to the User Profiles page
        return redirect(reverse('user_list'))
