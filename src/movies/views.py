from django.db import models as db_models
# from rest_framework.response import Response
# from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import permissions

from . import models, service
from .serializers import (MovieListSerializer,
                          MovieDetailSerializer,
                          ReviewCreateSerializer,
                          RatingCreateSerializer,
                          ActorListSerializer,
                          ActorDetailSerializer,
                          )


# class MovieListView(APIView):
#     """Вывод списка фильмов"""

    # # def get(self, request):
    # #     movies = models.Movie.objects.filter(draft=False)
    # #     serializer = MovieListSerializer(instance=movies, many=True)
    # #     return Response(serializer.data)
    #
    # # def get(self, request):
    # #     movies = models.Movie.objects.filter(draft=False).annotate(
    # #         rating_user=db_models.Case(
    # #             db_models.When(ratings__ip=service.get_client_ip(request), then=True),
    # #             default=False,
    # #             output_field=db_models.BooleanField()
    # #         ),
    # #     )
    # #     serializer = MovieListSerializer(movies, many=True)
    # #     return Response(serializer.data)
    #
    # def get(self, request):
    #     movies = models.Movie.objects.filter(draft=False).annotate(
    #         rating_user=db_models.Count('ratings', filter=db_models.Q(ratings__ip=service.get_client_ip(request)))
    #     ).annotate(
    #         # avg_star=db_models.Sum(db_models.F('ratings__star')) / db_models.Count(db_models.F('ratings'))
    #         avg_star=db_models.Avg('ratings__star') + 0.5 # "+0.5" чтобы int() в сериализаторе округлил по математически
    #     )
    #     serializer = MovieListSerializer(movies, many=True)
    #     return Response(serializer.data)


class MovieListView(ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = service.MovieFilter
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        movies = models.Movie.objects.filter(draft=False).annotate(
                rating_user=db_models.Count(
                    'ratings',
                    filter=db_models.Q(ratings__ip=service.get_client_ip(self.request))),
            ).annotate(
                avg_star=db_models.Avg('ratings__star') + 0.5
            )
        return movies


# class MovieDetailView(APIView):
#     """Вывод фильмоа"""
#
#     def get(self, request, pk):
#         movie = models.Movie.objects.get(pk=pk, )
#         serializer = MovieDetailSerializer(instance=movie)
#         return Response(serializer.data)


class MovieDetailView(RetrieveAPIView):
    """Вывод фильмоа"""
    serializer_class = MovieDetailSerializer
    # queryset = models.Movie.objects.filter(draft=False)

    def get_queryset(self):
        return models.Movie.objects.filter(draft=False)

# class ReviewCreateView(APIView):
#     """Добавление отзыва"""
#
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data, )
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


class ReviewCreateView(CreateAPIView):
    """Добавление отзыва"""
    serializer_class = ReviewCreateSerializer


# class RatingCreateView(APIView):
#     """Добавление рейтинга"""
#
#     def post(self, request):
#         serializer = RatingCreateSerializer(data=request.data)
#         print(request.POST)
#         if serializer.is_valid():
#             serializer.save(ip=service.get_client_ip(request=request))
#             return Response(status=201)
#         else:
#             return Response(status=400)


class RatingCreateView(CreateAPIView):
    """Добавление рейтинга"""
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(ip=service.get_client_ip(request=self.request))



class ActorListView(ListAPIView):
    """Вывод списка актеров и режисеров"""
    queryset = models.Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(RetrieveAPIView):
    """Вывод списка актеров и режисеров"""
    queryset = models.Actor.objects.all()
    serializer_class = ActorDetailSerializer
