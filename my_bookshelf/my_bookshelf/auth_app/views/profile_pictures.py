from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.models import ProfilePicture


class ProfilePictureCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = ProfilePicture
    template_name = 'auth_app/profile_picture_add.html'
    fields = ('picture',)

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfilePictureChangeView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = ProfilePicture
    template_name = 'auth_app/profile_picture_change.html'
    fields = ('picture',)

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})


class ProfilePictureDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = ProfilePicture
    template_name = 'auth_app/profile_picture_delete.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})
