from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import New, News, Subscription
from .forms import NewForm
from .filters import NewFilter
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.db.models import Exists, OuterRef



class NewsList(ListView):
    model = New
    ordering = 'name'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
class NewDetail(DetailView):
    model = New
    template_name = 'new.html'
    context_object_name = 'new'


class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_new',)
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_new',)
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'


class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_new',)
    model = New
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        news_id = request.POST.get('news_id')
        news = News.objects.get(id=news_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, news=news)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                news=news,
            ).delete()

    news_with_subscriptions = News.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                news=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'news': news_with_subscriptions},
    )
