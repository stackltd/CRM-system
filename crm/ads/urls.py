from django.urls import path

from .views import (
    AdCreateView,
    AdDeleteView,
    AdDetailView,
    AdsList,
    AdStatisticView,
    AdUpdateView,
)

app_name = "ads"

urlpatterns = [
    path("", AdsList.as_view(), name="ads-list"),
    path("new/", AdCreateView.as_view(), name="ad-create"),
    path("<int:pk>/delete/", AdDeleteView.as_view(), name="ad-delete"),
    path("<int:pk>/", AdDetailView.as_view(), name="ad-detail"),
    path("<int:pk>/edit/", AdUpdateView.as_view(), name="ad-update"),
    path("statistic/", AdStatisticView.as_view(), name="ad-statistic"),
]
