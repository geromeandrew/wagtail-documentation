from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.db import models
import mammoth
from bs4 import BeautifulSoup
from wagtail.images.models import Image
from wagtail.documents.models import Document

from django.utils.text import slugify
from django.core.files.base import ContentFile
import base64

class ParagraphBlock(blocks.RichTextBlock):
    class Meta:
        icon = 'doc-full'
        label = 'Paragraph'

    def __init__(self, required=False, **kwargs):
        super().__init__(required=required, **kwargs)

class ImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'image'
        label = 'Image'

    def __init__(self, required=False, **kwargs):
        super().__init__(required=required, **kwargs)

class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=[
        ('python', 'Python'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('javascript', 'Javascript'),
    ], required=False)
    code = blocks.TextBlock(required=False)

    class Meta:
        icon = 'code'
        label = 'Code'

class HeadingBlock(blocks.StructBlock):
    level = blocks.ChoiceBlock(choices=[
        ('1', 'Heading 1'),
        ('2', 'Heading 2'),
        ('3', 'Heading 3'),
    ], default='1')
    text = blocks.CharBlock(required=False)

    class Meta:
        icon = 'title'
        label = 'Heading'

class ListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(blocks.CharBlock(required=False), **kwargs)

    class Meta:
        label = 'List Item'

class TableBlock(blocks.StructBlock):
    headers = blocks.ListBlock(blocks.CharBlock(required=False), label='Headers', required=False)
    rows = blocks.ListBlock(
        blocks.ListBlock(blocks.CharBlock(required=False), label='Row', required=False),
        label='Rows',
        required=False
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
    child = blocks.ListBlock(FifthChildBlock(), required=False)

class ThirdChildBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    content = blocks.RichTextBlock(required=False)
    child_img = ImageBlock(required=False)
    child = blocks.ListBlock(FourthChildBlock(), required=False)
        
class SecondChildBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    content = blocks.RichTextBlock(required=False)
    child_img = ImageBlock(required=False)
    child = blocks.ListBlock(ThirdChildBlock(), required=False)
        
class FirstChildBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    content = blocks.RichTextBlock(required=False)
    child_img = ImageBlock(required=False)
    child = blocks.ListBlock(SecondChildBlock(), required=False)

class TreeBlock(blocks.StructBlock):
    children = blocks.ListBlock(FirstChildBlock(), required=False)

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

    heading_texts = models.TextField(blank=True, editable=False)

    word_file = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('word_file'),
    ]

    def _parse_nested_list(self, element):
        """
        Recursively parse nested list elements (<ul> and <li>) into TreeBlock structure,
        mapping content to 'content' and images to 'child_img'.
        """
        def parse_list_item(li_element):
            title = li_element.text.strip()  
            child_img = None 
            content = title  

            img_tag = li_element.find('img', recursive=False)
            if img_tag:
                if img_tag['src'].startswith('data'):
                    _, image_data = img_tag['src'].split(',', 1)
                    image_name = img_tag.get('alt', 'uploaded_image')
                    image = Image(file=ContentFile(base64.b64decode(image_data), name=f"{slugify(image_name)}.png"))
                    image.save()
                    child_img = image
                else:
                    image = Image.objects.filter(file=img_tag['src']).first()
                    if image:
                        child_img = image

            children_ul = li_element.find('ul', recursive=False)  
            child_blocks = []

            if children_ul:
                child_li_items = children_ul.find_all('li', recursive=False)
                for child_li in child_li_items:
                    child_blocks.append(parse_list_item(child_li))

            return {
                'title': title,  
                'content': content,
                'child_img': child_img,
                'child': child_blocks  
            }

        parsed_items = []
        li_elements = element.find_all('li', recursive=False)
        for li_element in li_elements:
            parsed_items.append(parse_list_item(li_element))

        return parsed_items

    def save(self, *args, **kwargs):
        if self.word_file:
            document_path = self.word_file.file.path
            with open(document_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html_content = result.value

            soup = BeautifulSoup(html_content, "html.parser")

            stream_data = []

            if soup:
                for element in soup.children:
                    if element.name == "p":
                        if element.find("img"):
                            img_tag = element.find("img")
                            if img_tag['src'].startswith('data'):
                                _, image_data = img_tag['src'].split(',', 1)
                                image_name = img_tag.get('alt', 'uploaded_image')
                                image = Image(file=ContentFile(base64.b64decode(image_data), name=f"{slugify(image_name)}.png"))
                                image.save()
                                stream_data.append(("image", image))
                        else:
                            stream_data.append(("paragraph", element.text))

                    elif element.name in ["h1", "h2", "h3"]:
                        level = element.name[-1]
                        stream_data.append(("heading", {"level": level, "text": element.text}))

                    elif element.name == "table":
                        headers = [th.text for th in element.find_all("th")]
                        rows = [[td.text for td in tr.find_all("td")] for tr in element.find_all("tr")]
                        stream_data.append(("table", {"headers": headers, "rows": rows}))

                    elif element.name in ["ol", "ul"]:
                        li_list = element.find_all('li', recursive=False)
                        
                        if li_list and li_list[0].find('strong', recursive=False):
                            strong_tag = li_list[0].find('strong', recursive=False)
                            print("Header Value:", strong_tag.text)
                            stream_data.append(("heading", {"level": "1", "text": strong_tag.text}))

                        items = [li.text for li in element.find_all("li", recursive=False) if not li.find('strong', recursive=False)]
                        print('li list:', items)
                        
                        stream_data.append(("list", items))

                        if any(li.find('ul') or li.find('ol') for li in li_list):
                            tree_data = self._parse_nested_list(element)
                            stream_data.append(("tree", {"children": tree_data}))

                    elif element.name == "img":
                        if element['src'].startswith('data'):
                            _, image_data = element['src'].split(',', 1)
                            image_name = element.get('alt', 'uploaded_image')
                            image = Image(file=ContentFile(base64.b64decode(image_data), name=f"{slugify(image_name)}.png"))
                            image.save()
                            stream_data.append(("image", image))
                        else:
                            img = Image.objects.filter(file=element['src']).first()
                            if img:
                                stream_data.append(("image", img))

                self.body = self.body.stream_block.to_python(stream_data)
            else:
                raise ValueError("No valid content found in the Word document.")

        headings = []
        for block in self.body:
            if block.block_type == 'heading':
                headings.append(block.value['text'])

        self.heading_texts = '\n'.join(headings)

        super().save(*args, **kwargs)




