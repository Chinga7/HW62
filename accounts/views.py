from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from accounts.forms import UserRegistrationForm


class RegisterView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = 'user_create.html'

    def form_valid(self, form):
        user = form.save()
        # Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse('webapp:project_list')

