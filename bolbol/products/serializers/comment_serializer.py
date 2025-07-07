from rest_framework import serializers
from products.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_masked_fullname = serializers.CharField(source="author.get_masked_fullname", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "author_masked_fullname",
            "text",
            "posted_at"
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]

    def create(self, validated_data):
        validated_data["author"] = self.context["author"]
        validated_data["product"] = self.context.get("product")
        return super().create(validated_data)