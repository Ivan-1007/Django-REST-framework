from abc import ABC

from rest_framework import serializers

from .models import Movie, Review, Rating, RatingStar, Actor


class ActorListSerializer(serializers.ModelSerializer):
    """Вывод актеров"""

    class Meta:
        model = Actor
        fields = ('id', 'name',)


class ActorDetailSerializer(serializers.ModelSerializer):
    """Вывод описания актера"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'age', 'description', 'image')


class MovieListSerializer(serializers.ModelSerializer):
    """Список Фильмов"""
    rating_user = serializers.BooleanField()
    avg_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'category', 'rating_user', 'avg_star')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавить отзыв"""
    class Meta:
        model = Review
        fields = '__all__'


class RecursiveSerializer(serializers.Serializer):
    """Вывод дочерних отзывов"""

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    """Возвращает отзывы у которых нет родителей"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewListSerializer(serializers.ModelSerializer):
    """Вывод отзывов"""

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('id', 'name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детали фильма"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    # actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    directors = ActorDetailSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft', )


class RatingCreateSerializer(serializers.ModelSerializer):
    """Добавление рейтинга к фильму"""

    class Meta:
        model = Rating
        fields = ('star', 'movie', )

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={
                'star': validated_data.get('star')
            }
        )
        return rating


