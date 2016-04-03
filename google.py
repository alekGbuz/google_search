import urllib.request
from bs4 import BeautifulSoup

class GoogleResponse():
    def __init__(self,response_text,response_url):
        self.text = response_text
        self.url = response_url

class GoogleRequest():
    google_url = 'https://www.google.com/search?q='
    start = '&start='
    def __init__(self,search = 'google',search_depth = 1):
        self.search = search
        self.search_depth = search_depth

    def convert_search_words(self):
        words = []
        word = ''
        for i in self.search:
            if i.isdigit() or i.isalpha():
                word += i
            else:
                words.append(word)
                word=''
        words.append(word)
        return '+'.join(words)

    def search_google(self,search_page):
        search_page = str(search_page)+'0' if search_page != 0 else ''
        req = urllib.request.Request(
            self.google_url+self.convert_search_words()+search_page,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'
             }
            )
        html = urllib.request.urlopen(req).read()
        page = BeautifulSoup(html,'html.parser')
        response_blocks =  page.find_all('h3',{'class':'r'})
        return response_blocks

    def get_google_response(self):
        response_blocks = []
        resp = []
        for i in range(self.search_depth):
            response_blocks += self.search_google(i)
        for block in response_blocks:
            a = block.find('a')
            resp.append(GoogleResponse(a.text,a.get('href')))
        return resp

def main():
    gr = GoogleRequest('Minsk Vilna',2)
    for g in gr.get_google_response():
        print (g.text)
        print (g.url)

main()

