from django.urls import path
from .views import NewsList, NewDetail, NewCreate, NewUpdate, NewDelete, subscriptions


urlpatterns = [
   path('', NewsList.as_view(), name='new_list'),
   path('<int:pk>', NewDetail.as_view(), name='new_detail'),
   path('create/', NewCreate.as_view(), name='new_create'),
   path('<int:pk>/update/', NewUpdate.as_view(), name='new_update'),
   path('<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]

