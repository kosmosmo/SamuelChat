import urllib.request
from bs4 import BeautifulSoup
import json,re,collections
import bulk,upload
class Scraper():
    def __init__(self):
        self.path = 'download/'
        self.dlurl = 'http://101soundboards.com/storage/board_sounds/'
        self.format = '.mp3'
        self.convert = 'convert/'
        pass

    def get_soup(self, url, header):
        return BeautifulSoup(urllib.request.urlopen(url), 'html.parser')

    def scraper(self,url):
        infos = collections.defaultdict(str)
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = self.get_soup(url, header)
        result = re.search('var board_data_preload = (.*)\;', soup.text)
        result =  json.loads(result.group(1))
        for item in result["sounds"]:
            infos[item['id']] = item['sound_transcript']
        return infos

    def downloader(self,dic):
        for k,v in dic.items():
            words = v.split(' ')
            for i in range(len(words)):
                if words[i] and words[i][0].isalpha():
                    words[i] = words[i].lower()
            v = re.sub('[^A-Za-z0-9]+', '',''.join(words))
            url = self.dlurl+str(k)+self.format
            urllib.request.urlretrieve(url,self.path+v+self.format)
            print (v)

    def converter(self):
        bulk.bulkConverter(self.path,self.convert).main()
    
    def upload(self):
        upload.s3upload(self.convert).run()

        


a = Scraper()
a.downloader(a.scraper('https://www.101soundboards.com/boards/10336'))
a.converter()
a.upload()