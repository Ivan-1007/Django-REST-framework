from django.db import models as db_models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from . import models, service
from .serializers import (MovieListSerializer,
                          MovieDetailSerializer,
                          ReviewCreateSerializer,
                          RatingCreateSerializer,
                          ActorListSerializer,
                          ActorDetailSerializer,
                          )


class MovieListView(APIView):
    """Вывод списка фильмов"""

    # def get(self, request):
    #     movies = models.Movie.objects.filter(draft=False)
    #     serializer = MovieListSerializer(instance=movies, many=True)
    #     return Response(serializer.data)

    # def get(self, request):
    #     movies = models.Movie.objects.filter(draft=False).annotate(
    #         rating_user=db_models.Case(
    #             db_models.When(ratings__ip=service.get_client_ip(request), then=True),
    #             default=False,
    #             output_field=db_models.BooleanField()
    #         ),
    #     )
    #     serializer = MovieListSerializer(movies, many=True)
    #     return Response(serializer.data)

    def get(self, request):
        movies = models.Movie.objects.filter(draft=False).annotate(
            rating_user=db_models.Count('ratings', filter=db_models.Q(ratings__ip=service.get_client_ip(request)))
        ).annotate(
            # avg_star=db_models.Sum(db_models.F('ratings__star')) / db_models.Count(db_models.F('ratings'))
            avg_star=db_models.Avg('ratings__star') + 0.5 # "+0.5" чтобы int() в сериализаторе округлил по математически
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Вывод фильмоа"""

    def get(self, request, pk):
        movie = models.Movie.objects.get(pk=pk, )
        serializer = MovieDetailSerializer(instance=movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Добавление отзыва"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data, )
        if review.is_valid():
            review.save()
        return Response(status=201)


class RatingCreateView(APIView):
    """Добавление рейтинга"""

    def post(self, request):
        serializer = RatingCreateSerializer(data=request.data)
        print(request.POST)
        if serializer.is_valid():
            serializer.save(ip=service.get_client_ip(request=request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorListView(ListAPIView):
    """Вывод списка актеров и режисеров"""
    queryset = models.Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(RetrieveAPIView):
    """Вывод списка актеров и режисеров"""
    queryset = models.Actor.objects.all()
    serializer_class = ActorDetailSerializer
