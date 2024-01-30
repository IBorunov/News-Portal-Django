from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, User
from .filters import PostFilter
from .forms import PostForm, ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
class PostList(ListView, LoginRequiredMixin):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'Authors').exists()
        return context

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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path =='/newsportal/articles/create/':
            post.type = 'A'
        post.save()
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ProfileUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = ProfileForm
    model = User
    template_name = 'profile_edit.html'
@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        author_group.user_set.add(user)
    register=Author.objects.create(user=request.user)
    register.save()
    return redirect('/newsportal/')