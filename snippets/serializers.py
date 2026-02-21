from rest_framework.reverse import reverse
from rest_framework import serializers

from .models import Snippet, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title"]


class SnippetSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
    )

    tag_details = TagSerializer(source="tags", many=True, read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = [
            "id",
            "title",
            "note",
            "created_at",
            "updated_at",
            "tags",
            "tag_details",
            "detail_url",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        return reverse(
            "snippet-detail",
            kwargs={"pk": obj.pk},
            request=request,
        )

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        user = self.context["request"].user

        snippet = Snippet.objects.create(
            created_by=user,
            **validated_data,
        )

        for tag_title in tags_data:
            tag, _ = Tag.objects.get_or_create(title=tag_title)
            snippet.tags.add(tag)

        return snippet

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)

        instance.title = validated_data.get("title", instance.title)
        instance.note = validated_data.get("note", instance.note)
        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            for tag_title in tags_data:
                tag, _ = Tag.objects.get_or_create(title=tag_title)
                instance.tags.add(tag)

        return instance
