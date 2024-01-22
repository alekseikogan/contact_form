from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import AddPostForm, ContactForm, LoginUserForm, RegisterUserForm
from .models import Category, Women
from .utils import DataMixin


ANONYMOUS_USER_PK = 3
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

class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['cat_selected'] = 0
        return context

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

class WomenDetail(DetailView):
    model = Women
    template_name = 'women/show_post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        context['cat_selected'] = Women.objects.get(
            slug=self.kwargs['post_slug']).cat_id
        return context


def about(request):
    return render(
        request,
        'women/about.html',
        context={'title': 'О сайте', 'menu': menu}
        )


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

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.user:
                form.save(commit=False).author_id = request.user.pk
                form.save()
            else:
                print('Пользователь НЕ зареган.')
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
        context['title'] = 'Регистрация'
        context['menu'] = menu
        return context


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

class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория ' + str(context['posts'][0].cat)
        context['cat_selected'] = Category.objects.get(
            slug=self.kwargs['cat_slug']).pk
        context['menu'] = menu
        return context

    def get_queryset(self):
        return Women.objects.filter(
            cat__slug=self.kwargs['cat_slug'],
            is_published=True).select_related('cat')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self) -> str:
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')
