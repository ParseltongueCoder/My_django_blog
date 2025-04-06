from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from .models import Post, HeroBanner
from django.core.paginator import Paginator


# Function-based view for the homepage
def home(request):
    now = timezone.now()
    hero_banner = HeroBanner.objects.filter(start_date__lte=now, end_date__gte=now).first()
    posts_list = Post.objects.all()                # Retrieve all posts
    paginator = Paginator(posts_list, 5)             # Divide posts into pages with 5 posts per page
    page_number = request.GET.get('page')           # Get current page number from URL query parameter
    posts = paginator.get_page(page_number)         # Retrieve the posts for the current page
    context = {
        'posts': posts,
        'hero_banner': hero_banner,
    }
    return render(request, 'blog/home.html', context)


# Class-based view for post detail
class PostDetailView(DetailView):
    model = Post


# Class-based view for creating a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Class-based view for updating an existing post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Class-based view for deleting a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
