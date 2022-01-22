import urllib
import requests
import json

def getpage(pageNumber:int) -> dict:
    r = requests.get(f'https://external.api.yle.fi/v1/teletext/pages/{pageNumber}.json?app_id=ef64cfef&app_key=5b2b993030bbb3537a23f1a058cbbeda')
    if len(r.text)>0:
        return json.loads(r.text)

# Hardcoded page numbers. Lazy way to go about it, but who cares about talousuutiset or weather from teletext?    
uutiset_kotimaa = 102
uutiset_ulkomaat = 130
uutiset_kotimaa = getpage(uutiset_kotimaa)
uutiset_ulkomaat = getpage(uutiset_ulkomaat)

news = {}
for newsPage in [uutiset_kotimaa, uutiset_ulkomaat]:
    for item in newsPage['teletext']['page']['subpage'][0]['content'][0]['line']:
        text_items = []
        if 'Text' in item.keys(): 
            textlist = item['Text'].split()
            for i, token in enumerate(textlist): 
                try:
                    num = int(token)
                    # Again, who cares about talous
                    if not 'TALOUS' in textlist:
                        text_items.append([num, ' '.join(textlist[i+1:])])
                    break
                except ValueError: 
                    continue
        if len(text_items)==0: continue
        for pagenumber, headline in text_items: 
            newspage = getpage(pagenumber)
            if not newspage: continue
            count = 0
            result = []
            for item in newspage['teletext']['page']['subpage'][0]['content'][0]['line']: 
                if 'Text' in item.keys(): 
                    count += 1
                    if count  >2: 
                        result.append(item['Text'].strip())
            news.update({pagenumber: {'Name': headline, 'Text': result}})

            

for pagenumber, newsdict in news.items(): 
    print(f'-----{pagenumber}-----')
    for name, text in newsdict.items(): 
        jointext = ''.join(text)
        print(f'{jointext}\n')