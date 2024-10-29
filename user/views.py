from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from user.forms import RegisterForm
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from blogs.models import Post
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from blogs.forms import PostForm

# Vista para el registro de usuarios
class UserRegistration(FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:success')

    def form_valid(self, form):
        user = form.save()
        return super(UserRegistration, self).form_valid(form)

# Función para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('users:login')

# Vista del perfil del usuario
@login_required
def user_profile(request):
    return render(request, 'users/user_profile.html', {'user': request.user})

# Vista de las publicaciones del usuario
@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user)  # Filtrar publicaciones del usuario
    return render(request, 'users/user_posts.html', {'posts': posts})

# Vista para crear una nueva publicación
class CreatePostView(LoginRequiredMixin, FormView):
    model = Post
    template_name = 'users/create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('users:user_posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = 'users/success_registration.html'