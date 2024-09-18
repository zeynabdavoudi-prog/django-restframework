from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile, User
from django.shortcuts import get_object_or_404


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='Snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    category = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Category.objects.all())
    author = serializers.SlugRelatedField(many=False, slug_field='first_name', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet', None)
        else:
            rep.pop('context', None)
            rep.pop('created_date', None)
            rep.pop('updated_date', None)
            rep.pop('status', None)
            rep.pop('relative_url', None)
        return rep

    def create(self, validated_data):
        user = get_object_or_404(User, id=self.context.get('request').user.id)
        validated_data['author'] = get_object_or_404(Profile, user=user)
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
