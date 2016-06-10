from time import sleep
import quickfix as fix


class MyApplication(fix.Application):
    acceptor = None
    sessionID = None

    def dd(self):
        settings = self.acceptor.getSessionSettings(self.sessionID)
        return fix.DataDictionary(settings.getString("DataDictionary"))

    def getFieldName(self, mess):
        return self.dd().getFieldName(mess.getField(), "")[0]
    def parse(self, mess):
        field = mess.getField()
        value = mess.getValue()
        dd = self.dd()
        return (dd.getFieldName(field, "")[0],
                dd.getValueName(field, value, "")[0])

    def onCreate(self, sessionID): return
    def onLogout(self, sessionID): return
    def toAdmin(self, sessionID, message): return
    def fromAdmin(self, message, sessionID): return
    def toApp(self, sessionID, message): return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print 'Welcome, trader!'

    def fromApp(self, message, sessionID):

        msgtype = fix.MsgType()
        symbol = fix.Symbol()
        side = fix.Side()
        ordtype = fix.OrdType()
        text = fix.Text()

        message.getHeader().getField(msgtype)
        message.getField(symbol)
        message.getField(side)
        message.getField(ordtype)
        message.getField(text)
        print
        print 'Message received! It reads:'
        print ' = '.join(self.parse(msgtype))
        print self.getFieldName(symbol), '=', symbol.getString()
        print ' = '.join(self.parse(side))
        print ' = '.join(self.parse(ordtype))
        print self.getFieldName(text), '=', text.getString()

    def run(self, acceptor):
        self.acceptor = acceptor
        sleep(60)

fileName = 'exchange_settings.ini'
settings = fix.SessionSettings(fileName)

app = MyApplication()

storeFactory = fix.FileStoreFactory(settings)
logFactory = fix.FileLogFactory(settings)

acceptor = fix.SocketAcceptor(app, storeFactory, settings, logFactory)
acceptor.start()

app.run(acceptor)

acceptor.stop()
