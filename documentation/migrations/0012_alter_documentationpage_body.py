# Generated by Django 5.0.9 on 2024-09-16 07:17

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0011_alter_documentationpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentationpage',
            name='body',
            field=wagtail.fields.StreamField([('paragraph', 0), ('image', 1), ('code', 4), ('heading', 7), ('list', 8), ('table', 12), ('tree', 25)], blank=True, block_lookup={0: ('documentation.models.ParagraphBlock', (), {}), 1: ('documentation.models.ImageBlock', (), {}), 2: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('python', 'Python'), ('html', 'HTML'), ('css', 'CSS'), ('javascript', 'Javascript')]}), 3: ('wagtail.blocks.TextBlock', (), {}), 4: ('wagtail.blocks.StructBlock', [[('language', 2), ('code', 3)]], {}), 5: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('1', 'Heading 1'), ('2', 'Heading 2'), ('3', 'Heading 3')]}), 6: ('wagtail.blocks.CharBlock', (), {}), 7: ('wagtail.blocks.StructBlock', [[('level', 5), ('text', 6)]], {}), 8: ('documentation.models.ListBlock', (), {}), 9: ('wagtail.blocks.ListBlock', (6,), {'label': 'Headers'}), 10: ('wagtail.blocks.ListBlock', (6,), {'label': 'Row'}), 11: ('wagtail.blocks.ListBlock', (10,), {'label': 'Rows'}), 12: ('wagtail.blocks.StructBlock', [[('headers', 9), ('rows', 11)]], {}), 13: ('wagtail.blocks.CharBlock', (), {'max_length': 255, 'required': False}), 14: ('wagtail.blocks.RichTextBlock', (), {'required': False}), 15: ('wagtail.blocks.StructBlock', [[('title', 13), ('child_img', 1), ('content', 14)]], {}), 16: ('wagtail.blocks.ListBlock', (15,), {}), 17: ('wagtail.blocks.StructBlock', [[('title', 13), ('content', 14), ('child_img', 1), ('child', 16)]], {}), 18: ('wagtail.blocks.ListBlock', (17,), {}), 19: ('wagtail.blocks.StructBlock', [[('title', 13), ('content', 14), ('child_img', 1), ('child', 18)]], {}), 20: ('wagtail.blocks.ListBlock', (19,), {}), 21: ('wagtail.blocks.StructBlock', [[('title', 13), ('content', 14), ('child_img', 1), ('child', 20)]], {}), 22: ('wagtail.blocks.ListBlock', (21,), {}), 23: ('wagtail.blocks.StructBlock', [[('title', 13), ('content', 14), ('child_img', 1), ('child', 22)]], {}), 24: ('wagtail.blocks.ListBlock', (23,), {}), 25: ('wagtail.blocks.StructBlock', [[('children', 24)]], {})}),
        ),
    ]
