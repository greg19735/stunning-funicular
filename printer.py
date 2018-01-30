import websiteObj

class SitePrinter(object):

    def __init__(self,originalSite, pageMapList):
        self.originalSite = originalSite
        if pageMapList is None:
            pageMapList = []
        self.pageMapList = pageMapList

    def printPage(self):
        f = open("prints/" + self.originalSite.filename + "." +  self.originalSite.ext, 'w')
        f.write('OriginPage	LinkToPage	LinkToPageStatus	LinkToPageTitle	OriginPageDate	OriginPageTitle\n')
        for page in self.pageMapList:
            f.write(page.OriginPage + '\t' + page.LinkToPage + '\t' + page.LinkToPageStatus + '\t' + page.LinkToPageTitle + '\t' + page.OriginPageDate + '\t' + page.OriginPageTitle + '\n' )



