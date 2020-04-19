import pprint
from googleapiclient.discovery import build

def getImage(wikiPage, title): 
    apiKey = 'AIzaSyDAWePqwREeikzXA9XsHwyy0yHRyOaSVp4'
    searchEngineId = '017551383683576584532:ckswlkvxiin'
    query = str(wikiPage + ' ' + title)
    print(query)

    service = build("customsearch", "v1",
                developerKey=apiKey)

    res = service.cse().list(
        q=query,
        cx=searchEngineId,
        searchType='image',
        num=3,
        imgType='photo',
        imgSize='large',
        fileType='jpg',
        safe= 'off',
        # rights='cc_noncommercial'
    ).execute()
    # print(res)
    if not 'items' in res:
        res = service.cse().list(
            q=wikiPage,
            cx=searchEngineId,
            searchType='image',
            num=2,
            imgType='photo',
            imgSize='large',
            # fileType='png',
            safe= 'off'
        ).execute()
        print(res['items'][0]['title'])
        print(res['items'][0]['link'])
        if 'instagram' in res['items'][0]['link']:
            return res['items'][1]['link']
        return res['items'][0]['link']
    else:
        if 'instagram' in res['items'][0]['link']:
            return res['items'][1]['link']
        return res['items'][0]['link']

# getImage('endodontia', 'história')