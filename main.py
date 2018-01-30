
from functions import checkLinks
from functions import getLinks
from websiteObj import WebsiteObj
from printer import SitePrinter
from pagemap import PageMap
from functions import linkTranslator
from functions import checkLink
from functions import codeTranslate

from functions import checkWhiteList

import datetime

now = datetime.datetime.now()


#Sites to be crawled. All in different files.
originSites = [WebsiteObj("https://www.epa.gov/fedfac/brac-dashboard",'fedfac','txt', "https://www.epa.gov"),
               WebsiteObj("https://www.epa.gov/environmental-topics",'topics','txt', "https://www.epa.gov"),
               WebsiteObj("https://www.epa.gov/laws-regulations", 'laws', 'txt', "https://www.epa.gov") ]

#originSites = [WebsiteObj("https://www.epa.gov/environmental-topics",'topics','txt', "https://www.epa.gov")]

linksToCrawl = []

whitelist = []
connectionDict = {}
crawledList = []



for webpage in originSites:
    #seed list
    domain = webpage.url
    linksToCrawl = []
    linksToCrawl.append(domain)



    #go through each link
    pageLinks = []
    pageMapList = []

    crawlcount = 0

    for crawllink in linksToCrawl:
        print("percentage done = " + str(crawlcount) + " / " + str(len(linksToCrawl)))
        crawlcount = crawlcount+1
        # check for whitelist (run before)
        #newpage = not checkWhiteList(crawllink, whitelist)

        pageLinks = getLinks(crawllink,pageLinks)
        pageLinks = linkTranslator(crawllink, pageLinks, webpage.tld)

        crawledList.append(crawllink)


        linkcount = 0
        #linkPageMap = PageMap()
        #test links
        for linkURL in pageLinks:
            #check for used link
            if linkURL in connectionDict:
                code = connectionDict[linkURL]
            else:
                code = checkLink(linkURL)
                connectionDict[linkURL] = code

            codeString = codeTranslate(str(code))
            pagemap = PageMap(linkURL, crawllink, codeString, "title1", now.strftime("%Y-%m-%d %H:%M"), "title2")
            pageMapList.append(pagemap)
            #check to see if link should be crawled

            if(str(linkURL).startswith(domain) and codeString == "Success"):
                if(str(linkURL) not in crawledList):
                    linksToCrawl.append(str(linkURL))










    PageToPrint = SitePrinter(webpage, pageMapList)
    PageToPrint.printPage()


