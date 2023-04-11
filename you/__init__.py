from tls_client   import Session
from re         import findall
from json       import loads, dumps
from uuid       import uuid4
from fake_useragent import UserAgent
from requests.cookies import RequestsCookieJar

ua = UserAgent()

class Completion:
    def create(
        prompt          : str,
        page            : int  = 1,
        count           : int  = 10,
        safeSearch      : str  = "Moderate",
        onShoppingpage  : bool = False,
        mkt             : str  = "",
        responseFilter  : str  = "WebPages,Translations,TimeZone,Computation,RelatedSearches",
        domain          : str  = "youchat",
        queryTraceId    : str  = None,
        chat            : list = [],
        includelinks    : bool = False,
        detailed        : bool = False,
        debug           : bool = False ) -> dict:
        
        cookies2 = RequestsCookieJar()
        cookies2.set('safesearch_guest', 'Moderate')
        cookies2.set('uuid_guest', str(uuid4()))
        client         = Session(client_identifier="chrome110")
        
        client.cookies = cookies2

        client.headers = {
            "authority"         : "you.com",
            "accept"            : "text/event-stream",
            "accept-language"   : "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
            "cache-control"     : "no-cache",
            "referer"           : "https://you.com/search?q=who+are+you&tbm=youchat",
            "sec-ch-ua"         : '"Not_A Brand";v="99", "Google Chrome";v="110", "Chromium";v="110"',
            "sec-ch-ua-mobile"  : "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest"    : "empty",
            "sec-fetch-mode"    : "cors",
            "sec-fetch-site"    : "same-origin",
            "cookie"           : f'safesearch_guest=Moderate; uuid_guest={str(uuid4())}',
            "user-agent"        : ua.chrome
        }
        print(ua.chrome)
        response = client.get(f"https://you.com/api/streamingSearch",  params = {
                "q"              : prompt,
                "page"           : page,
                "count"          : count,
                "safeSearch"     : safeSearch,
                "onShoppingPage" : onShoppingpage,
                "mkt"            : mkt,
                "responseFilter" : responseFilter,
                "domain"         : domain,
                "queryTraceId"   : str(uuid4()) if queryTraceId is None else queryTraceId,
                "chat"           : str(chat),  # {"question":"","answer":" '"}
            }
        )
        
        print(response.status_code)
        
        if debug:
            print('\n\n------------------\n\n')
            print(response.text)
            print('\n\n------------------\n\n')

        youChatSerpResults      = findall(r'youChatSerpResults\ndata: (.*)\n\nevent', response.text)[0]
        thirdPartySearchResults = findall(r"thirdPartySearchResults\ndata: (.*)\n\nevent", response.text)[0]
        slots                   = findall(r"slots\ndata: (.*)\n\nevent", response.text)[0]
        
        text = response.text.split('}]}\n\nevent: youChatToken\ndata: {"youChatToken": "')[-1]
        text = text.replace('"}\n\nevent: youChatToken\ndata: {"youChatToken": "', '')
        text = text.replace('event: done\ndata: I\'m Mr. Meeseeks. Look at me.\n\n', '')
        
        extra = {
            'youChatSerpResults'      : loads(youChatSerpResults),
            'slots'                   : loads(slots)
        }

        return {
            'response': text,
            'links'   : loads(thirdPartySearchResults)['search']["third_party_search_results"] if includelinks else None,
            'extra'   : extra if detailed else None,
        }
