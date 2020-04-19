import wikipediaapi
import json
from template2 import generateSlidesSubCategory, generateSlidesCategory,getSlideCover,removeSlidesModel

def getWikipediaTerm(SLIDES, DECK_ID):
        wiki_wiki = wikipediaapi.Wikipedia(
                language='pt',
                extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        wikiPage = "Correntina"
        p_wiki = wiki_wiki.page(wikiPage)
        # print(p_wiki.sections[0].title)
        # print(p_wiki.sections[0].title)
        sections = (p_wiki.sections)
        getSlideCover(wikiPage,SLIDES,DECK_ID)
        getWikipediaCategories(wikiPage,SLIDES, DECK_ID, sections, level=0)
        removeSlidesModel(SLIDES, DECK_ID)

def getWikipediaCategories(wikiPage,SLIDES, DECK_ID,sections, level=0):
        for s in sections:
                title = s.title
                content = s.text[0:300]
                cat = ("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:300]))
                print(cat)
                if '**' in str(cat):
                        generateSlidesSubCategory(wikiPage,SLIDES, DECK_ID, title, content)
                        getWikipediaCategories(wikiPage,SLIDES, DECK_ID,s.sections, level + 1)
                else:
                        generateSlidesCategory(wikiPage,SLIDES, DECK_ID,title,content)
                        getWikipediaCategories(wikiPage,SLIDES, DECK_ID,s.sections, level + 1)
                
def print_sections(sections, level=0):
        for s in sections:
                cat = ("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
                print(cat)
                if '**'in str(cat):
                        print_sections(s.sections, level + 1)
                else:
                        print_sections(s.sections, level + 1)