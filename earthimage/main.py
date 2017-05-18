
import requests
import random, re , threading , time , socket
import tornado.web
import tornado.ioloop


allindex = 0

def getUrl():
    id = randomid()
    with open('date', 'r') as f:
        _image = f.read()

    _imagelist = _image.split(',')
    _imagelist.pop()
    return _imagelist[id]


def updateindex():
    global  allindex
    with open('daterand', 'r') as f:
        allindex = f.read()

def getAllDate():
    print('getAllDate')
    reponse = requests.get('https://raw.githubusercontent.com/limhenry/earthview/master/earthview.json')
    html = reponse.text

    with open('date', 'w') as f:
        imageList = re.findall('"image":".*?"' , html)
        for image in imageList:
            imageurl = re.findall('[0-9]{4,5}' ,image)
            f.write(imageurl[0] + ',')

    with open('daterand', 'w') as f:
        f.write(str(len(imageList)))

    updateindex()

    time.sleep(60 * 60 * 24)
    getAllDate()


def randomid():
    global allindex
    _allindex = int(allindex)
    id = random.randint(0, _allindex)
    return id


class earthImage(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        _id = getUrl()
        imageurl = 'http://www.gstatic.com/prettyearth/assets/full/%s.jpg'%(_id)
        print(imageurl)
        self.redirect(imageurl)



application = tornado.web.Application([
    (r"/earthImage" , earthImage)
])

def runServer():
    port = 9011
    application.listen(port)

    localIP = socket.gethostbyname(socket.gethostname())
    print("run in %s:%s"%(localIP,port))
    tornado.ioloop.IOLoop.instance().start()

def startServer():
    print('startServer')
    runServer()



def main():
    updateindex()

    thread_getInfoDate = threading.Thread(target=getAllDate, name='getAllDate')
    thread_startServer = threading.Thread(target=startServer, name='startServer')

    thread_getInfoDate.start()
    thread_startServer.start()



main()


