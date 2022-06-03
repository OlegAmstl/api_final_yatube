from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         default=serializers.CurrentUserDefault(),
#         slug_field='username',
#         read_only=True
#     )
#     following = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all()
#
#     )
#
#     class Meta:
#         fields = '__all__'
#         model = Follow
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following'),
#                 message='Нельзя подписываться на себя.'
#             )
#         ]
#
#         def validate(self, data):
#             if self.context.get('request').user == data['following']:
#                 raise serializers.ValidationError("Нельзя подписаться на себя")
#             return data


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        required=False,
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    def validate(self, data):
        if self.context.get('request').user == data['following']:
            raise serializers.ValidationError("Нельзя подписаться на себя")
        return data

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=['user', 'following']
            )
        ]



