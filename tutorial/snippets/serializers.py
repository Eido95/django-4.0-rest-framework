from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet


# Provide a way of serializing and deserializing the snippet instances
# into representations such as json.
class SnippetSerializer(serializers.ModelSerializer):
    # Serializer is replicated a lot of information that's also contained in
    # the Snippet model, ModelSerializer solves it.
    # ModelSerializer classes don't do anything particularly magical,
    # they are simply a shortcut for creating serializer classes

    # Used only for serialized representations (not for updating model
    # instances when they are deserialized)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        # We add an explicit field for 'snippets' because 'snippets' is
        # a reverse relationship on the User model (it will not be included
        # by default when using the ModelSerializer class)
        fields = ['id', 'username', 'snippets']


# python manage.py shell
# 1. Creates a couple of code snippets to work with.
#
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
#
# snippet = Snippet(code='foo = "bar"\n')
# snippet.save()
#
# snippet = Snippet(code='print("hello, world")\n')
# snippet.save()
#
#
# 2.Serializing Snippet instance
#
# serializer = SnippetSerializer(snippet)
# serializer.data
#
#
# 3. Render the serialized data into json
#
# content = JSONRenderer().render(serializer.data)
# content
#
#
# 4. Render json data to deserializable data
#
# import io
#
# stream = io.BytesIO(content)
# data = JSONParser().parse(stream)
#
#
# 5. Deserializing Snippet data and save it
#
# serializer = SnippetSerializer(data=data)
# serializer.is_valid()  # True
# serializer.validated_data  # OrderedDict([('title', ''), ...])
# serializer.save()  # <Snippet: Snippet object>
#
#
# 6. Inspect all the fields in a serializer instance
#
# from snippets.serializers import SnippetSerializer
# serializer = SnippetSerializer()
# print(repr(serializer))
#
