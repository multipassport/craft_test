from django.urls import path

from mailings import views

urlpatterns = [
    path(
        'customers/',
        views.CustomerCreateView.as_view(),
        name='icon-list',
    ),
    path(
        'customers/<int:pk>/',
        views.CustomerUpdateDestroyView.as_view(),
        name='icon-detail',
    ),
    path(
        'mailings/',
        views.MailingCreateView.as_view(),
        name='icon-list',
    ),
    path(
        'mailings/<int:pk>/',
        views.MailingUpdateDestroyView.as_view(),
        name='icon-detail',
    ),
    path(
        'mailings/<int:pk>/stats/',
        views.MailingStatsView.as_view(),
        name='mailing-stats-detail',
    ),
    path(
        'stats/',
        views.TotalStatsView.as_view(),
        name='stats-list',
    ),
]
