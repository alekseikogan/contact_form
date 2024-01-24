from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import AddPostForm, ContactForm, LoginUserForm, RegisterUserForm
from .models import Women
from .utils import DataMixin


ANONYMOUS_USER_PK = 2
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}]


# def index(request):
#     posts = Women.objects.all()
#     context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0
#     }
#     return render(
#         request,
#         'women/index.html',
#         context=context
#     )

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/show_post.html', context)

class WomenDetail(DataMixin, DetailView):
    model = Women
    template_name = 'women/show_post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_selected = context['post'].cat_id
        c_def = self.get_user_context(
            title=context['post'],
            cat_selected=cat_selected)
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
            # form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(
#         request,
#         'women/addpage.html',
#         context={'title': 'Добавление статьи', 'menu': menu, 'form': form})

class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.user:
                form.save(commit=False).author_id = request.user.pk
                form.save()
            else:
                form.save(commit=False).author_id = ANONYMOUS_USER_PK
                form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'menu': menu,
        'title': 'Обратная связь'
        }
    return render(request, 'women/contact.html', context=context)


def contact_success(request):
    context = {
        'menu': menu,
        'title': 'Успешно отправлено'
        }
    return render(request, 'women/contact_success.html', context=context)


# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)
#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'title': 'Рубрики',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': posts[0].cat_id,
#     }
#     return render(request, 'women/index.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_selected = context['posts'][0].cat_id
        c_def = self.get_user_context(
            title='Категория ' + str(context['posts'][0].cat),
            cat_selected=cat_selected)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(
            cat__slug=self.kwargs['cat_slug'],
            is_published=True).select_related('cat')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def about(request):
    return render(
        request,
        'women/about.html',
        context={'title': 'О сайте', 'menu': menu}
        )


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
