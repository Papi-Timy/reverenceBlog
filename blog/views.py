from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Count, Q
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
import random
import urllib.parse
# Create your views here.


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_category_count():
    queryset = Post.objects.values(
        'categories__title', 'categories__image').annotate(Count('categories__title')).order_by('categories__title')[0:3]
    return queryset


def index(request):
    category_title = get_category_count()
    cat_trend = Category.objects.order_by('-image')

    post = Post.objects.all()
    latest = Post.objects.order_by("-timestamp")[1:4]

    first_post = Post.objects.first()
    category = Category.objects.all()
    qoute = Qoutes.objects.first()

    paginator = Paginator(post, 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_qs = paginator.page(page)
    except PageNotAnInteger:
        paginated_qs = paginator.page(1)
    except EmptyPage:
        paginated_qs = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        email = request.POST.get('email')
        new_signup = SignUp()
        new_signup.email = email
        new_signup.save()

    context = {
        'queryset': paginated_qs,
        'paginator': paginator,
        'page_request_var': page_request_var,
        'latest_post': latest,
        'category': category,
        'cat_trend': cat_trend,
        'category_title': category_title,
        'first_post': first_post,
        'qoutes': qoute
    }
    return render(request, 'blog/index.html', context)


def nav(request):
    category = Category.objects.all()

    context = {
        'category': category
    }
    return render(request, 'blog/base.html', context)


def blog_column(request, slug):
    category_title = get_category_count()
    cat_trend = Category.objects.order_by('-image')
    latest = Post.objects.order_by("-timestamp")[1:4]
    cat = Post.objects.filter(categories__slug=slug)
    if cat.exists():
        paginator = Paginator(cat, 5)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)

        try:
            paginated_qs = paginator.page(page)
        except PageNotAnInteger:
            paginated_qs = paginator.page(1)
        except EmptyPage:
            paginated_qs = paginator.page(paginator.num_pages)
    else:
        return HttpResponse('<h1>No category found </h1>')

    category = Category.objects.all()

    context = {
        'queryset': paginated_qs,
        'category': cat,
        'category': category,
        'paginator': paginator,
        'latest_post': latest,
        'cat_trend': cat_trend,
        'page_request_var': page_request_var

    }
    return render(request, 'blog/blog_column.html', context)


def search(request):
    post_list = Post.objects.all()
    category_title = get_category_count()
    latest = Post.objects.order_by("-timestamp")[1:4]
    cat_trend = Category.objects.order_by('-image')
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(post_list, 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_qs = paginator.page(page)
    except PageNotAnInteger:
        paginated_qs = paginator.page(1)
    except EmptyPage:
        paginated_qs = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_qs,
        'page_request_var': page_request_var,
        'latest_post': latest,
        'paginator': paginator,
        'cat_trend': cat_trend,
        'category_title': category_title
    }
    return render(request, 'blog/search.html', context)


def post(request, slug):
    post = Post.objects.filter(slug=slug)
    share_string = urllib.parse.quote("ghhhhhhgk", safe='')
    category_title = get_category_count()
    latest = Post.objects.order_by("-timestamp")[1:4]
    cat_trend = Category.objects.order_by('-image')
    if post.exists():
        post = post.first()
    else:
        return HttpResponse("<h1> Page not Found </h1>")

    category = Category.objects.all()
    qoute = Qoutes.objects.first()
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            form.instance.post = post
            form.save()
            return redirect(reverse("blog_app:post-detail", kwargs={
                'slug': post.slug
            }))

    context = {
        'post': post,
        'share_string': share_string,
        'categories': category,
        'form': form,
        'category_title': category_title,
        'cat_trend': cat_trend,
        'latest_post': latest,

        'category': category,
        'qoutes': qoute
    }
    return render(request, 'blog/post1.html', context)


def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    title = 'update'
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse(
                "blog_app:post-detail",
                kwargs={
                    'id': form.instance.id
                }
            ))
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'blog/post_create.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse(
        "blog_app:blog_column"))

    return render(request, 'blog/post_create.html', context)


def post_create(request):
    title = 'create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse(
                "blog_app:post-detail",
                kwargs={
                    'id': form.instance.id
                }
            ))
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'blog/post_create.html', context)


def contact(request):
    category = Category.objects.all()
    cat_trend = Category.objects.order_by('-image')

    context = {
        'category': category,
        'cat_trend': cat_trend,

    }
    return render(request, 'blog/contact.html', context)
