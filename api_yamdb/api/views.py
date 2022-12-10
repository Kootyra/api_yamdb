from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as djfilters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .const import EMAIL_SENDER
from .permissions import Admin, IsAdminOrReadOnly, IsAuthorModerAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, NewUserAdmin, ReviewSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          UserConfirmationSerializer, UserProfileSerializer,
                          UserRegistrationSerializer)


class CategoryViewSet(viewsets.GenericViewSet, CreateModelMixin,
                      DestroyModelMixin, ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(viewsets.GenericViewSet, CreateModelMixin,
                   DestroyModelMixin, ListModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleFilter(djfilters.FilterSet):
    name = djfilters.CharFilter(field_name='name', lookup_expr='contains')
    genre = djfilters.CharFilter(field_name='genre', lookup_expr='slug')
    category = djfilters.CharFilter(field_name='category', lookup_expr='slug')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    filterset_class = TitleFilter
    ordering = ['-id']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(Avg('reviews__score'))


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModerAdminOrReadOnly,)
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModerAdminOrReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return Comment.objects.filter(review=review)


class UserRegistration(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def signup(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(User,
                                 username=serializer.validated_data["username"]
                                 )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Registration code',
            f'Для получения токена введите код {confirmation_code}',
            f'{EMAIL_SENDER}',
            [serializer.data.get('email')],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserConfirmation(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def confirmation(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_form = serializer.initial_data.get('username')
        user = get_object_or_404(User, username=user_form)
        if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]
        ):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = NewUserAdmin
    permission_classes = (Admin,)

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=UserProfileSerializer,
    )
    def profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
