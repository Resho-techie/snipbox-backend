from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Snippet, Tag
from .serializers import SnippetSerializer, TagSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Snippet.objects.filter(created_by=self.request.user).prefetch_related(
            "tags"
        )

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["get"])
    def overview(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "total_snippets": queryset.count(),
                "snippets": serializer.data,
            }
        )


class TagViewSet(viewsets.ViewSet):

    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        tag = get_object_or_404(Tag, pk=pk)
        snippets = tag.snippets.filter(created_by=request.user)
        serializer = SnippetSerializer(
            snippets, many=True, context={"request": request}
        )
        return Response(serializer.data)
