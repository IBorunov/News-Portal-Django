from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy

class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'


class PostSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path =='newsportal/articles/create/':
            post.type = 'A'
        post.save()
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')