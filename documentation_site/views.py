import mammoth
from django.http import HttpResponse

from bs4 import BeautifulSoup

def convert_docx_mammoth_to_html(request): 
    # Path to the .docx file 
    docx_file = 'documentation_site/static/nested.docx' 
    # Custom style map 
    custom_style_map = """table => table.table-bordered""" 
     
 
    # Convert .docx to HTML 
    with open(docx_file, 'rb') as file: 
        result = mammoth.convert_to_html(file, style_map=custom_style_map) 
        html_content = result.value 
        
        soup = BeautifulSoup(html_content, "html.parser")
        # print('soup: ', soup)
        for element in soup.children:  
            
            # if element.name == "ol" and element.name == "li" and element.find('strong'):
            #     print("element", element)
                
            if element.name == "ol":  # Check if the element is an ordered list
                li_list = element.find_all('li', recursive=False)  # Find all <li> tags directly within the <ol>
                if li_list[0].find('strong', recursive=False):
                    strong_tag = li_list[0].find('strong', recursive=False)
                    print("Valueee:", strong_tag.text)  # Get the text inside the <strong>
 
        styled_html = f""" 
        <html> 
        <head> 
            <style> 
                .table-bordered {{ 
                    border-collapse: collapse; 
                    margin: auto; 
                }} 
                .table-bordered, .table-bordered td, .table-bordered th {{ 
                    border: 1px solid black; 
                }} 
            </style> 
        </head> 
        <body> 
            {soup} 
        </body> 
        </html> 
        """ 
 
    # Return HTML as HttpResponse 
    return HttpResponse(styled_html)