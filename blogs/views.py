from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import generic, View
from django.utils.text import slugify
from django.views.generic import FormView , DetailView, UpdateView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from blogs.models import Post, Category, Rating
from django.utils import timezone
from django.db.models import Q, Count
from django.urls import reverse, reverse_lazy
from blogs.forms import PostCommentForm, PostForm

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'blogs/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Consulta que obtiene los posts ordenados por el número de valoraciones
        top_rated_posts = Post.objects.filter(pub_date__lte=timezone.now()).annotate(
            num_ratings=Count('ratings')
        ).order_by('-num_ratings')[:3]  # Limita a los 3 primeros o cuantos prefieras
        
        # Actualiza el campo `featured` para los posts con más valoraciones
        Post.objects.filter(id__in=[post.id for post in top_rated_posts]).update(featured=True)
        
        context['post_list'] = Post.objects.filter(pub_date__lte=timezone.now())
        context['categories'] = Category.objects.all()
        context['featured'] = Post.objects.filter(featured=True).filter(pub_date__lte=timezone.now())[:3]
        return context

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.exclude(hidden_by_users__user=self.request.user)
        context['form'] = PostCommentForm()
        return context
    
    
class PostRatingView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        stars = int(request.POST.get('stars', 0))
        
        # Verifica si el usuario ya ha valorado este post
        rating, created = Rating.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={'stars': stars}
        )
        
        return JsonResponse({
            'stars': rating.stars,
            'average_rating': post.average_rating
        })

class PostCommentFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'blogs/post_detail.html'
    form_class = PostCommentForm
    model = Post

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Obtenemos el post al que está asociado el comentario
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user  # Asignamos el autor del comentario
        comment.post = self.object  # Asignamos el post al comentario
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogs:post', kwargs={'slug': self.object.slug}) + '#comments-section'

class PostDetailWithCommentsView(LoginRequiredMixin, DetailView, FormView):
    model = Post
    template_name = 'blogs/post_detail.html'
    form_class = PostCommentForm
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.post = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('blogs:post', kwargs={'slug': self.object.slug}) + '#comments-section'


class PostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentFormView.as_view()
        return view(request, *args, **kwargs)

class FeaturedListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blogs/results.html'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(featured=True).filter(pub_date__lte=timezone.now())

class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blogs/results.html'
    paginate_by = 2

    def get_queryset(self):
        query = self.kwargs.get('slug')  # Obtiene el slug de la URL
        return Post.objects.filter(categorias__slug=query).filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('slug')  # Obtiene la categoría actual
        return context

class SearchResultsView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blogs/results.html'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(categorias__title__icontains=query)
        ).filter(pub_date__lte=timezone.now()).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search')
        return context
    
@user_passes_test(lambda u: u.is_superuser)
def create_category(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Category.objects.create(title=title, slug=slugify(title))
        return redirect(reverse('users:create_post'))
    

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/edit_post.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('blogs:post', kwargs={'slug': self.object.slug})

class DeletePostView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blogs/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blogs:home_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context
    


class OtherPostsView(UserPassesTestMixin, generic.ListView):
    model = Post
    template_name = 'blogs/other_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        # Obtener todas las publicaciones y contar los comentarios
        return Post.objects.filter(pub_date__lte=timezone.now(), featured=False).annotate(num_comments=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_superuser'] = self.request.user.is_superuser
        context['title'] = 'Otras Publicaciones'
        
        # Filtrar posts destacados y actualizarlos según las valoraciones
        top_rated_posts = Post.objects.filter(pub_date__lte=timezone.now()).annotate(
            num_ratings=Count('ratings')
        ).order_by('-num_ratings')[:3]
        
        Post.objects.filter(id__in=[post.id for post in top_rated_posts]).update(featured=True)
        
        context['featured_posts'] = Post.objects.filter(featured=True).order_by('-pub_date')
        context['most_commented_post'] = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments').first()
        
        return context