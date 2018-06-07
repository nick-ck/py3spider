import requests
from bs4 import BeautifulSoup
import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Mzitu():
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"}

    def request(self, url):
        content = requests.get(url, headers=self.headers)
        return content

    def all_url(self, url):
        html = self.request(url)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        all_a = all_a[1:]
        print(all_a)
        for a in all_a:
            title = a.get_text()
            print(u'开始保存', title)
            path = str(title).replace('?', '_')
            self.mkdir(path)
            href = a['href']
            print(title,href)
            self.html(href)

    def html(self, href):
        html = self.request(href)
        self.headers['referer'] = href
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi') \
            .find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)

    def img(self, page_url):
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', 'main-image') \
            .find('img')['src']
        self.save(img_url)

    def save(self, img_url):
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join(basedir, path))
        if not isExists:
            print(r'创建了一个名字叫做' + path + u'文件夹')
            os.makedirs(os.path.join(basedir, path))
            os.chdir(os.path.join(basedir, path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

#TODO:add subprocess thread

mzitu = Mzitu()
mzitu.all_url('http://www.mzitu.com')
