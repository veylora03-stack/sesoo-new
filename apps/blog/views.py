from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from .models import Post, Category, Tag

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.filter(status='published').select_related('category')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('order')
        context['q'] = self.request.GET.get('q', '')
        context['current_category'] = None
        context['current_tag'] = None
        context['page_title'] = f"جستجو: {context['q']}" if context['q'] else "وبلاگ"
        return context

class PostCategoryView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        return Post.objects.filter(status='published', category=self.category).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('order')
        context['current_category'] = self.category
        context['current_tag'] = None
        context['page_title'] = self.category.title
        return context

class PostTagView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(status='published', tags=self.tag).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('order')
        context['current_tag'] = self.tag
        context['current_category'] = None
        context['page_title'] = f"تگ: {self.tag.title}"
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        Post.objects.filter(pk=self.object.pk).update(view_count=F('view_count') + 1)
        self.object.refresh_from_db()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['related_posts'] = Post.objects.filter(
            status='published', category=post.category
        ).exclude(pk=post.pk)[:3]
        context['gallery'] = post.images.filter(is_active=True).order_by('order')
        return context