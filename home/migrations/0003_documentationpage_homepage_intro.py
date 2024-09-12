# Generated by Django 5.0.9 on 2024-09-11 05:45

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('paragraph', 0), ('image', 1), ('code', 4), ('heading', 5)], blank=True, block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {}), 1: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 2: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('python', 'Python'), ('html', 'HTML'), ('css', 'CSS'), ('javascript', 'Javascript')]}), 3: ('wagtail.blocks.TextBlock', (), {}), 4: ('wagtail.blocks.StructBlock', [[('language', 2), ('code', 3)]], {'icon': 'code', 'label': 'Code'}), 5: ('wagtail.blocks.CharBlock', (), {'form_classname': 'title'})})),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
