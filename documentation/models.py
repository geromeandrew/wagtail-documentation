from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.db import models

class ParagraphBlock(blocks.RichTextBlock):
    class Meta:
        icon = 'doc-full'
        label = 'Paragraph'

class ImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'image'
        label = 'Image'

class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=[
        ('python', 'Python'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('javascript', 'Javascript'),
    ])
    code = blocks.TextBlock()

    class Meta:
        icon = 'code'
        label = 'Code'

class HeadingBlock(blocks.StructBlock):
    level = blocks.ChoiceBlock(choices=[
        ('1', 'Heading 1'),
        ('2', 'Heading 2'),
        ('3', 'Heading 3'),
    ], default='1')
    text = blocks.CharBlock()

    class Meta:
        icon = 'title'
        label = 'Heading'

class ListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(blocks.CharBlock(), **kwargs)

    class Meta:
        label = 'List Item'

class TableBlock(blocks.StructBlock):
    headers = blocks.ListBlock(blocks.CharBlock(), label='Headers')
    rows = blocks.ListBlock(
        blocks.ListBlock(blocks.CharBlock(), label='Row'),
        label='Rows'
    )

    class Meta:
        icon = 'table'
        label = 'Table'


class FifthChildBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    child_img = ImageBlock(required=False)
    content = blocks.RichTextBlock(required=False)

class FourthChildBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    content = blocks.RichTextBlock(required=False)
    child_img = ImageBlock(required=False)
    child = blocks.ListBlock(FifthChildBlock())

class ThirdChildBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    content = blocks.RichTextBlock(required=False)
    child_img = ImageBlock(required=False)
    child = blocks.ListBlock(FourthChildBlock())
        
class SecondChildBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    content = blocks.RichTextBlock(required=False)
    child_img = ImageBlock(required=False)
    child = blocks.ListBlock(ThirdChildBlock())
        
class FirstChildBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    content = blocks.RichTextBlock(required=False)
    child_img = ImageBlock(required=False)
    child = blocks.ListBlock(SecondChildBlock())

class TreeBlock(blocks.StructBlock):
    children = blocks.ListBlock(FirstChildBlock())

    class Meta:
        icon = "list-ul"
        label = "Tree Node"


class DocumentationPage(Page):
    body = StreamField([
        ('paragraph', ParagraphBlock()),
        ('image', ImageBlock()),
        ('code', CodeBlock()),
        ('heading', HeadingBlock()),
        ('list', ListBlock()),
        ('table', TableBlock()),
        ('tree', TreeBlock()),
    ], blank=True)

    # Store headings as a list of strings
    heading_texts = models.TextField(blank=True, editable=False)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def save(self, *args, **kwargs):
        # Extract all heading texts from StreamField and save them in heading_texts
        headings = []
        for block in self.body:
            if block.block_type == 'heading':
                headings.append(block.value['text'])
        self.heading_texts = '\n'.join(headings)  # Store as newline-separated text
        super().save(*args, **kwargs)