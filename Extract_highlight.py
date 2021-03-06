### Code by Technical Sid (https://technicalsid.com)

from typing import List, Tuple
import re
import fitz

# function to parse highlighted text

def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    # print(annot)
    # pno = re.findall(r'^\D*(\d+)', str(annot))
    # print(pno)
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        # where the highlighted part is
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences.append(" ".join(w[4] for w in words))

    pno = re.findall(r'^\D*(\d+)', str(annot))
    pno = ",".join(pno)
    sentences.append(pno)
    sentences.append(annot.colors["stroke"])
    # sentence = " ".join(sentences)
    # sentence.append(sentences)
    return sentences

# function to handle multiple pages

def handle_page(page):
    wordlist = page.getText("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x
    # page_ = page
    # print(page_)
    highlights = []
    annot = page.firstAnnot
    # print(annot)
    # print(annot)
    while annot:
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
            # highlights.append(annot.colors["stroke"])
            # highlights.append(page)
        # highlights.append(page)
        annot = annot.next
    return highlights

# function to extract comments
def extract_comments(doc):
    comment_list = []
    pno = ''
    comment_colors = []
    
    for i in range(doc.pageCount):
        page = doc[i]
        for annot in page.annots():
            comment_ = []
            if annot.info["content"] != '':
                pno = re.findall(r'^\D*(\d+)', str(page))
                pno = ",".join(pno)

                # comment_colors.append(annot.colors["stroke"])
                comment_.append(annot.info["content"])
                comment_.append(pno)
                comment_.append(annot.colors["stroke"])

                # comment_.append(annot.line_ends["xref"])
                comment_list.append(comment_)
                return comment_list
            
# main function            
def main(filepath: str) -> List:
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += (handle_page(page))
        # highlights.append(handle_page(page))

        # print(page)
    comments = extract_comments(doc)
    return highlights, comments

#Extracting highlighted text by passing pdf file to main function

highlight_list, comment_list = main("antibiotics_modified.pdf")

#Printing highlighted text
print(highlight_list)

#printing comments text
print(comment_list)