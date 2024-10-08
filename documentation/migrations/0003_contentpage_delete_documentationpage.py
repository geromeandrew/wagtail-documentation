# Generated by Django 5.0.9 on 2024-09-12 00:51

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0002_alter_documentationpage_body'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('heading', 2), ('paragraph', 3), ('image', 6), ('list', 9), ('code', 12), ('table', 17), ('nested_content', 18)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'max_length': 100, 'required': True}), 1: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('h1', 'Heading 1'), ('h2', 'Heading 2'), ('h3', 'Heading 3')]}), 2: ('wagtail.blocks.StructBlock', [[('heading_text', 0), ('heading_level', 1)]], {}), 3: ('documentation.models.ParagraphBlock', (), {}), 4: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': True}), 5: ('wagtail.blocks.CharBlock', (), {'max_length': 250, 'required': False}), 6: ('wagtail.blocks.StructBlock', [[('image', 4), ('caption', 5)]], {}), 7: ('wagtail.blocks.CharBlock', (), {'max_length': 100}), 8: ('wagtail.blocks.ListBlock', (7,), {}), 9: ('wagtail.blocks.StructBlock', [[('list_items', 8)]], {}), 10: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('python', 'Python'), ('javascript', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS')]}), 11: ('wagtail.blocks.TextBlock', (), {}), 12: ('wagtail.blocks.StructBlock', [[('language', 10), ('code', 11)]], {}), 13: ('wagtail.blocks.CharBlock', (), {}), 14: ('wagtail.blocks.ListBlock', (13,), {'label': 'Headers'}), 15: ('wagtail.blocks.ListBlock', (13,), {'label': 'Row'}), 16: ('wagtail.blocks.ListBlock', (15,), {'label': 'Rows'}), 17: ('wagtail.blocks.StructBlock', [[('headers', 14), ('rows', 16)]], {}), 18: ('wagtail.blocks.StreamBlock', [[('heading', 2), ('paragraph', 3), ('image', 6), ('list', 9), ('code', 12), ('table', 17)]], {'required': False})})),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.DeleteModel(
            name='DocumentationPage',
        ),
    ]
