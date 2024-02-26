from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import New
from .forms import NewForm
from .filters import NewFilter



class NewsList(ListView):
    model = New
    ordering = 'name'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novosti'] = "ТОЛЬКО СВЕЖАЯ ИНФОРМАЦИЯ!"
        return context
class NewDetail(DetailView):
    model = New
    template_name = 'new.html'
    context_object_name = 'new'

class NewCreate(CreateView):
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.type = 'AR'
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_title'] = self.get_type()['title']
        context['get_header'] = self.get_type()['header']
        return context

    def get_type(self):
        if self.request.path == '/articles/create/':
            return {'title': 'Create article', 'header': 'Добавить статью'}
        else:
            return {'title': 'Create news', 'header': 'Добавить новость'}

class NewUpdate(UpdateView):
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'

class NewDelete(DeleteView):
    model = New
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')

class NewCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'
