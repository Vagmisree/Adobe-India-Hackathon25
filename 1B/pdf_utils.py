from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, LAParams

def extract_sections_from_pdf(pdf_path):
    # Very basic heuristic based method that returns list of sections:
    # Each section is dict with keys: 'title', 'page', 'text'
    sections = []
    current_section = None
    laparams = LAParams(line_margin=0.3)
    for page_num, page_layout in enumerate(extract_pages(pdf_path, laparams=laparams), start=1):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                # Collect text lines and detect if a line looks like a heading (bold+large font heuristic)
                for line in element:
                    text = line.get_text().strip()
                    font_sizes = [c.size for c in line if isinstance(c, LTChar)]
                    avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 0
                    if avg_font_size > 12 and text:  # heuristic: font size >12 could be heading
                        if current_section:
                            sections.append(current_section)
                        current_section = {"title": text, "page": page_num, "text": ""}
                    else:
                        if current_section is None:
                            current_section = {"title": "Introduction", "page": page_num, "text": ""}
                        current_section["text"] += text + " "
    if current_section:
        sections.append(current_section)
    return sections
