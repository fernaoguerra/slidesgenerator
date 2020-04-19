import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import random
import uuid 
from images import getImage

# from wiki import term, author

def createDeck(credentials):
    TMPLFILE = 'base deck3'   # use your own!

    # DRIVE  = discovery.build('drive',  'v3', http=HTTP)
    DRIVE = googleapiclient.discovery.build('drive',  'v3', credentials=credentials)
    SLIDES = googleapiclient.discovery.build('slides', 'v1', credentials=credentials)

    rsp = DRIVE.files().list(q="name='%s'" % TMPLFILE).execute().get('files')[0]
    DATA = {'name': 'new slide'}
    print('** Copying template %r as %r' % (rsp['name'], DATA['name']))
    DECK_ID = DRIVE.files().copy(body=DATA, fileId=rsp['id']).execute().get('id')
    return SLIDES, DECK_ID

def removeSlidesModel(SLIDES, DECK_ID):
    #Delete initial Slides
    print('** Get slide objects, search for image placeholder')
    slide = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')
    print(slide[1]['objectId'])
    print(slide[2]['objectId'])
    print(slide[3]['objectId'])
    reqs = [
        {
        "deleteObject": {"objectId": slide[1]['objectId']
        }},
        {
        "deleteObject": {
            "objectId": slide[2]['objectId']
        }},
        {
        "deleteObject": {
            "objectId": slide[3]['objectId']
        }}
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},presentationId=DECK_ID, ).execute()
    print('DONE')

def getSlideCover(wikiPage,SLIDES,DECK_ID):
    #Slide1
    print('** Get slide objects, search for image placeholder')
    slide0 = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')[0]

    reqs = [
        {'replaceAllText': {
            'containsText': {'text': '{{title}}'},
            'replaceText': wikiPage,
            'pageObjectIds': slide0['objectId']
        }},
        {'replaceAllText': {
            'containsText': {'text': '{{author}}'},
            'replaceText': 'Fernão',
            'pageObjectIds': slide0['objectId']
        }},
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},presentationId=DECK_ID, ).execute()
    print('DONE')


def generateSlidesSubCategory(wikiPage,SLIDES,DECK_ID,title,content):
    #Slide1
    print('** Get slide objects, search for image placeholder')
    slide1 = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')[1]
    obj = None
    print(len(slide1['pageElements']))
    for obj in slide1['pageElements']:
        try:
            if 'RECTANGLE' in obj['shape']['shapeType']:
                break
        except:
            print('n tem')

    print('** Replacing placeholder text and icon')

    #Slide2
    print('** Get slide objects, search for image placeholder')
    slide2 = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')[2]
    obj = None
    print(len(slide2['pageElements']))
    for obj in slide2['pageElements']:
        try:
            if 'RECTANGLE' in obj['shape']['shapeType']:
                break
        except:
            print('n tem')
    
    img_url = getImage(wikiPage,title)
    # img_url= 'https://www.prefeitura.sp.gov.br/cidade/upload/Casa_Imagem_1334844048.jpg'

    print('** Replacing placeholder text and icon')
    
    pageId = slide1['objectId']
    lista = [str(slide1['objectId']) , str(slide2['objectId'])] 
    slideModel = random.choice(lista)

    reqs = [
        {
        "duplicateObject": {
            "objectId": slideModel,
            "objectIds": {
            pageId: str(uuid.uuid1())
            }
        }
        }
    ]

    r = SLIDES.presentations().batchUpdate(body={'requests': reqs},presentationId=DECK_ID).execute()
    r
    print((r))
    current_slide = (r['replies'][0]["duplicateObject"]["objectId"])
    print(current_slide)
    slides = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')
    for s in slides:
        if current_slide in s["objectId"]:   
            slidenovo = s
            continue
    # print(slidenovo["objectId"])
    obj = None
    for obj in slidenovo['pageElements']:
        try:
            if 'RECTANGLE' in obj['shape']['shapeType']:
                break
        except:
            print('n tem')

    reqs = [
        {'replaceAllText': {
            'containsText': {'text': '{{title}}'},
            'replaceText': title,
            'pageObjectIds': current_slide
        }},
        {'replaceAllText': {
            'containsText': {'text': '{{content}}'},
            'replaceText': content,
            'pageObjectIds': current_slide
        }},
        {'createImage': {
            'url': img_url,
            'elementProperties': {
                'pageObjectId': current_slide,
                'size': obj['size'],
                'transform': obj['transform'],
            }
        }},
        {'deleteObject': {'objectId': obj['objectId']}},
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},presentationId=DECK_ID, ).execute()
    print('tamanho ' + str((len(SLIDES.presentations().get(presentationId=DECK_ID,fields='slides').execute().get('slides')))))
    
    reqs = [
        {
        "updateSlidesPosition": {
            "slideObjectIds": [
                current_slide
            ],
            "insertionIndex": int((len(SLIDES.presentations().get(presentationId=DECK_ID,fields='slides').execute().get('slides')))-1)
            }
        }
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},presentationId=DECK_ID ).execute()
    print('DONE')


def generateSlidesCategory(wikiPage,SLIDES, DECK_ID,title,content):
    #Slide3
    print('** Get slide objects, search for image placeholder')
    slide3 = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')[3]
    obj = None
    print(len(slide3['pageElements']))
    for obj in slide3['pageElements']:
        try:
            if 'RECTANGLE' in obj['shape']['shapeType']:
                break
        except:
            print('n tem')
    
    img_url = getImage(wikiPage,title)
    # img_url= 'https://www.prefeitura.sp.gov.br/cidade/upload/Casa_Imagem_1334844048.jpg'

    print('** Replacing placeholder text and icon')
    
    pageId = slide3['objectId']

    reqs = [
        {
        "duplicateObject": {
            "objectId": pageId,
            "objectIds": {
            pageId: str(uuid.uuid1())
            }
        }
        }
    ]

    r = SLIDES.presentations().batchUpdate(body={'requests': reqs},presentationId=DECK_ID).execute()
    r
    print((r))
    current_slide = (r['replies'][0]["duplicateObject"]["objectId"])
    print(current_slide)
    slides = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')
    for s in slides:
        if current_slide in s["objectId"]:   
            slidenovo = s
            continue
    obj = None
    for obj in slidenovo['pageElements']:
        try:
            if 'RECTANGLE' in obj['shape']['shapeType']:
                break
        except:
            print('n tem')

    reqs = [
        {'replaceAllText': {
            'containsText': {'text': '{{category}}'},
            'replaceText': title,
            'pageObjectIds': current_slide
        }},
        {'replaceAllText': {
            'containsText': {'text': '{{content}}'},
            'replaceText': content,
            'pageObjectIds': current_slide
        }},
        {'createImage': {
            'url': img_url,
            'elementProperties': {
                'pageObjectId': current_slide,
                'size': obj['size'],
                'transform': obj['transform'],
            }
        }},
        {'deleteObject': {'objectId': obj['objectId']}},
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},presentationId=DECK_ID, ).execute()
    print('tamanho ' + str((len(SLIDES.presentations().get(presentationId=DECK_ID,fields='slides').execute().get('slides')))))
    
    reqs = [
        {
        "updateSlidesPosition": {
            "slideObjectIds": [
                current_slide
            ],
            "insertionIndex": int((len(SLIDES.presentations().get(presentationId=DECK_ID,fields='slides').execute().get('slides')))-1)
            }
        }
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},presentationId=DECK_ID ).execute()
    print('DONE')