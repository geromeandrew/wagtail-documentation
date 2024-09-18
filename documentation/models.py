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

    word_file = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('word_file'),
    ]
    
    def save(self, *args, **kwargs):
        if self.word_file:
            document_path = self.word_file.file.path
            with open(document_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html_content = result.value
            

            soup = BeautifulSoup(html_content, "html.parser")
            print('soup: ', soup)

            stream_data = []

            if soup:
                for element in soup.children:  
                    if element.name == "p":
                        stream_data.append(("paragraph", element.text))

                    elif element.name in ["h1", "h2", "h3"]:
                        level = element.name[-1] 
                        stream_data.append(("heading", {"level": level, "text": element.text}))

                    # elif element.name == "ul":
                    #     items = [li.text for li in element.find_all("li")]
                    #     stream_data.append(("list", items))

                    # elif element.name == "ol":
                    #     items = [li.text for li in element.find_all("li")]
                    #     stream_data.append(("ordered_list", items))

                    elif element.name == "table":
                        headers = [th.text for th in element.find_all("th")]
                        rows = [[td.text for td in tr.find_all("td")] for tr in element.find_all("tr")]
                        stream_data.append(("table", {"headers": headers, "rows": rows}))

                    elif element.name == "ol" or element.name == "ul":  # Check if the element is an ordered list
                        li_list = element.find_all('li', recursive=False)  # Find all <li> tags directly within the <ol>
                        if li_list[0].find('strong', recursive=False):
                            strong_tag = li_list[0].find('strong', recursive=False)
                            print("Header Valueee:", strong_tag.text)  
                            stream_data.append(("heading", {"level": "1", "text": strong_tag.text}))
                            
                         #   
                        items = [li.text for li in element.find_all("li", recursive=False) if not li.find('strong', recursive=False)]
                        print('li list: ', items)
                        stream_data.append(("list", items))
                            

                    elif element.name == "img":
                        img_src = element['src']
                        img = Image.objects.filter(file=img_src).first()
                        if img:
                            stream_data.append(("image", img))


                self.body = self.body.stream_block.to_python(stream_data)
            else:
                print("Error: No valid content found in the Word document.")
                raise ValueError("No valid content found in the Word document.")

        headings = []
        for block in self.body: 
            if block.block_type == 'heading':
                headings.append(block.value['text'])

        self.heading_texts = '\n'.join(headings)  #

        super().save(*args, **kwargs)

