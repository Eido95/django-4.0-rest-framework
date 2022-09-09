from rest_framework import serializers

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


# Provide a way of serializing and deserializing the snippet instances
# into representations such as json.
class SnippetSerializer(serializers.Serializer):
    # Fields that get serialized/deserialized
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # {'base_template': 'textarea.html'} flag is equivalent to using widget=widgets.Textarea
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


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
