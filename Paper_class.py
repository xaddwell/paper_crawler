from bs4 import BeautifulSoup as bs
import re

class security_Paper():
    def __init__(self, paper_title="", abstract="",
                 pdf_link="", paper_link="",
                 author="", slides_link=""):

        self.paper_title = self.parse_paper_title(paper_title)
        self.abstract = self.parse_paper_abstract(abstract)
        self.pdf_link = self.parse_paper_pdf_link(pdf_link)
        self.author = self.parse_paper_author(author)
        self.slides_link = self.parse_paper_slides_link(slides_link)
        self.paper_link = paper_link

    def parse_paper_title(self, paper_title):
        if len(paper_title) >= 1:
            doc = bs(str(paper_title[0]))
            paper_title = doc.find_all("h1")[0].text
            return paper_title

    def parse_paper_abstract(self, abstract):
        if len(abstract) >= 1:
            doc = bs(str(abstract[0]))
            abstract_paragraphs = doc.find_all("p")
            abstract = ""
            for paragraphs in abstract_paragraphs:
                abstract += paragraphs.text
                abstract += "\n"
            return abstract

    def parse_paper_pdf_link(self, pdf_link):
        if len(pdf_link) >= 1:
            pdf_link = pdf_link[0].find_all("a")[0]['href']
            return pdf_link

    def parse_paper_author(self, author):
        if len(author) >= 1:
            doc = bs(str(author[0]))
            author = doc.find_all("p")
            if len(author) >= 1:
                author = re.sub('<*>','',author[0].text)

            return author

    def parse_paper_slides_link(self, slides_link):
        if len(slides_link) >= 1:
            doc = bs(str(slides_link[0]))
            slides_link = doc.find_all("a")[0]['href']
            return slides_link


class ccs_Paper():
    def __init__(self, paper_title=None, abstract=None,
                 pdf_link=None, paper_link=None,
                 author=None, slides_link=None):

        self.paper_title = self.parse_paper_title(paper_title)
        self.abstract = self.parse_paper_abstract(abstract)
        self.pdf_link = self.parse_paper_pdf_link(pdf_link)
        self.author = self.parse_paper_author(author)
        self.slides_link = self.parse_paper_slides_link(slides_link)
        self.paper_link = paper_link

    def parse_paper_title(self, paper_title):
        if len(paper_title) >= 1:
            doc = bs(str(paper_title[0]))
            paper_title = doc.find_all("h1")[0].text
            print(paper_title)
            return paper_title

    def parse_paper_abstract(self, abstract):
        if len(abstract) >= 1:
            doc = bs(str(abstract[0]))
            abstract_paragraphs = doc.find_all("p")
            abstract = ""
            for paragraphs in abstract_paragraphs:
                abstract += paragraphs.text
                abstract += "\n"
        return abstract

    def parse_paper_pdf_link(self, pdf_link):
        return pdf_link

    def parse_paper_author(self, author):
        if len(author) >= 1:
            doc = bs(str(author[0]))
            author = doc.find_all("p")
            if len(author) >= 1:
                author = re.sub('<*>','',author[0].text)

        return author

    def parse_paper_slides_link(self, slides_link):
        if len(slides_link) >= 1:
            doc = bs(str(slides_link[0]))
            slides_link = doc.find_all("a")[0]['href']
            print(slides_link)
            return slides_link