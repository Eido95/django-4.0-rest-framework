from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet


# Provide a way of serializing and deserializing the snippet instances
# into representations such as json.
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # The HyperlinkedModelSerializer has the following differences from ModelSerializer:
    # It does not include the "id" field by default.
    # It includes a "url" field, using HyperlinkedIdentityField.
    # Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.

    # Used only for serialized representations (not for updating model
    # instances when they are deserialized)
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'title', 'code', 'linenos', 'language', 'style',
                  'owner', 'highlight']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        # We add an explicit field for 'snippets' because 'snippets' is
        # a reverse relationship on the User model (it will not be included
        # by default when using the ModelSerializer class)
        fields = ['url', 'id', 'username', 'snippets']


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
