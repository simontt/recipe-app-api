from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user-owned recipe attributes."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for current authenticated user only."""
        # Custom filtering of queryset
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new attribute."""
        # Is run just before saving a validated serializer,
        # so we can add user.
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database."""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, querystring):
        """Convert list of string ids to list of integers."""
        return [int(id) for id in querystring.split(',')]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        # Dictionary of query params provided in get request;
        # None if not provided
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')

        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # Django syntax for filtering on foreign key objects
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        # List for list view, detail for detail view
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        # Otherwise just return default serializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create new recipe."""
        serializer.save(user=self.request.user)

    # get_queryset etc. are default actions that we overwrote,
    # use action decorator to create custom actions!
    # detail=True means it works on one (detail) recipe.
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            # Just use save-function because we have a model-serializer
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        # errors is auto-generated if serializer not valid
        return Response(serializer.errors,
                        status.HTTP_400_BAD_REQUEST)
