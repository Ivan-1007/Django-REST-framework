from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie'),
    path('review/', views.ReviewCreateView.as_view(), name='create_review'),
    path('rating/', views.RatingCreateView.as_view(), name='create_rating'),
    path('actors/', views.ActorListView.as_view(), name='list'),
    path('actors/<int:pk>', views.ActorDetailView.as_view(), name='detail'),

]
