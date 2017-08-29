import requests
import re

class Bot(object):
    def __init__(self, wx):
        self.wechat = wx

    def ask(self, name, word):
        self._tuling123(name, word)

    def _tuling123(self, name, word):
        def _getImage(id, url):
            data = requests.get(url).content
            if data == '':
                return ''
            fn = 'img_tl_' + id + '.jpg'
            return self.wechat.saveFile(fn, data, 'webwxgetmsgimg')

        url = 'http://openapi.tuling123.com/openapi/api/v2'
        params = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": word
                },
                "inputImage": {
                    "url": ""
                }
            },
            "userInfo": {
                "apiKey": "8223d32db18541d4a99a34842a830fed",
                "userId": "132779"
            }
        }
        r = requests.post(url, json=params)
        res = r.json()
        images = []
        content = ''
        if res['results']:
            arr = res['results']
            for dic in arr:
                if (dic['resultType'] == 'image'):
                    images.append((dic['values']['silentState'], dic['values']['image']))
                else:
                    content += ','.join(dic['values'].values())
        else:
            content = '让我一个人静静 T_T...'

        for x in images:
            image = _getImage(x[0], x[1])
            print('自动回复: ' + x[1])
            if not self.wechat.sendImg(name, image):
                print('失败')

        print('自动回复: ' + content)
        if not self.wechat.sendMsg(name, content):
            print('失败')


    def _qingyunke(self, word):
        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % word
        r = requests.get(url)
        res = r.json()
        if res['result'] == 0:
            return res['content']
        else:
            return '让我一个人静静 T_T...'


    def _xiaodoubi(self, word):
        url = 'http://www.xiaodoubi.com/bot/chat.php'
        try:
            r = requests.post(url, data={'chat': word})
            return str(r.content)
        except:
            return "让我一个人静静 T_T..."


    def _simsimi(self, word, name):
        key = 'fa358fa1-4c58-48f3-9c7b-09c265668fcc'
        url = 'http://sandbox.api.simsimi.com/request.p?key=%s&lc=ch&ft=0.0&text=%s' % (
            key, word)
        r = requests.get(url)
        ans = r.json()
        content = '你在说什么，风太大听不清列'
        if ans['result'] == 100:
            content = ans['response']
        print('自动回复: ' + content)
        self.wechat.sendMsg(name, content)


    def searchContent(self, key, content, fmat='attr'):
        if fmat == 'attr':
            pm = re.search(key + '\s?=\s?"([^"<]+)"', content)
            if pm:
                return pm.group(1)
        elif fmat == 'xml':
            pm = re.search('<{0}>([^<]+)</{0}>'.format(key), content)
            if not pm:
                pm = re.search(
                    '<{0}><\!\[CDATA\[(.*?)\]\]></{0}>'.format(key), content)
            if pm:
                return pm.group(1)
        return '未知'
