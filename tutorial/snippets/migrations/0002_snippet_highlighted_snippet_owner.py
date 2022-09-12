# Generated by Django 4.0.7 on 2022-09-12 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def highlight_code(snippet):
    # Code copy-pasted because historical models:
    # https://docs.djangoproject.com/en/4.0/topics/migrations/#historical-models
    """
    Use the `pygments` library to create a highlighted HTML
    representation of the code snippet.
    """
    lexer = get_lexer_by_name(snippet.language)
    linenos = 'table' if snippet.linenos else False
    options = {'title': snippet.title} if snippet.title else {}
    formatter = HtmlFormatter(style=snippet.style, linenos=linenos,
                              full=True, **options)
    snippet.highlighted = highlight(snippet.code, lexer, formatter)


def forwards_blank_highlighted(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    snippet_class = apps.get_model("snippets", "Snippet")

    for snippet in snippet_class.objects.all():
        if not snippet.highlighted:
            highlight_code(snippet)
            snippet.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='highlighted',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='snippet',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(forwards_blank_highlighted, migrations.RunPython.noop)
    ]
