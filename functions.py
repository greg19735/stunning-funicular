from bs4 import BeautifulSoup
import urllib.request
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from linkobj import LinkObj
from pagemap import PageMap


def getLinks(url,pageLinks):
    print("Debug - getLinks url: " + url)
    linkList = []

    styleImports = 0

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    anchorList = []
    for a in soup.find_all('a'):
        try:
            anchor = LinkObj(a['href'], 'a', url )
            anchorList.append(anchor)
        except KeyError:
            print("keyerror")  # or some other fallback action


    lHrefList = []
    for l in soup.find_all('link', href=True):
        lLink = LinkObj(l['href'], 'l', url )
        lHrefList.append(lLink)

    scriptList = []
    for s in soup.find_all('script'):
       src = s.get('src')
       if src is not None:
           scriptobj = LinkObj(src, 'script', url )
           scriptList.append(scriptobj)

    imgList = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src is not None:
            imageobj = LinkObj(src, 'image', url)
            imgList.append(imageobj)

    pageLinks = anchorList + lHrefList + scriptList + imgList
    return pageLinks

def linkTranslator( url, pageLinks, tld):
    anchorList = []
    lHrefList = []
    scriptList = []
    imgList = []


    for link in pageLinks:
        if(str(link.url).endswith('/')):
            if(str(link.url) != '/'):
                link.url = link.url[:-1]


        if(link.linktype == 'a'):

            if(str(link.url).startswith('/')):
                if (str(link.url) != '/'):
                    anchorList.append(tld + link.url)

            elif(str(link.url).startswith('#')):
                pass
            else:
                anchorList.append(url)

        if (link.linktype == 'l'):
            if (str(link.url).startswith('/')):
                lHrefList.append(tld + link.url)
            elif (str(link.url).startswith('#')):
                pass
            else:
                lHrefList.append(url)

        if (link.linktype == 'script'):
            if (str(link.url).startswith('/')):
                scriptList.append(tld + link.url)
            elif (str(link.url).startswith('#')):
                pass
            else:
                scriptList.append(url)



        if (link.linktype == 'img'):
            if (str(link.url).startswith('/')):
                imgList.append(tld + link.url)
            elif (str(link.url).startswith('#')):
                pass
            else:
                imgList.append(url)

    pageLinks = anchorList + lHrefList + scriptList + imgList
    return pageLinks


def checkWhiteList(url, whitelist):

    if url in whitelist:
        print("checklist true: " + url)
        return True
    else:
        print("checklist false: " + url)
        return False

def checkLink(url):
    request = ""
    code= ""
    try:
        request = requests.get(url, verify=False)

        code = request.status_code
    except requests.exceptions.SSLError:
        print("SSL Error")

    return code




def codeTranslate(code):
    codeString = ""
    if(code.startswith('1')):
        codeString = "Informational"
    elif (code.startswith('2')):
        codeString = "Success"
    elif (code.startswith('3')):
        codeString = "Redirection"
    elif (code.startswith('4')):
        codeString = "Client Error"
    elif (code.startswith('5')):
        codeString = "Server Error"

    return codeString

def checkLinks(tld, parent, websiteLinks, visitedSites, anchorList,startURL ):
    print(anchorList)

    readylinks = []
    relative = []
    anchor = []
    other = []
    mailto = []

    #check for dupes


    for url in anchorList:
        if(url[0] == '/'):
            relative.append(tld + url)

        elif(url[0] == '#'):
            anchor.append(url)
        elif ("mailto" in url):
            mailto.append(url)
        elif ("http" in url):
            readylinks.append(url)
            if startURL in url:
                if (url not in visitedSites) and (url not in websiteLinks):
                    print(url)
                    websiteLinks.append(url)


        else:
            other.append(url)

    linksToTest = readylinks[0:20]
    print("NEXT PAGE")
    print(len(linksToTest))
    print(linksToTest)




    for l in linksToTest:

        try:
            request = requests.get(l, verify=False)

            visitedSites[l] = request.status_code
        except requests.exceptions.SSLError:
            print("SSL Error")




    print(visitedSites)