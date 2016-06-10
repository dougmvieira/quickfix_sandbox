from time import sleep
import quickfix as fix


def sendHelloWorldMessage(sessionID):
    message = fix.Message();
    header = message.getHeader();

    header.setField(fix.BeginString("FIX.4.1"))
    header.setField(fix.SenderCompID("HELLOWORLD_TRADER"))
    header.setField(fix.TargetCompID("HELLOWORLD_EXCHANGE"))
    header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    message.setField(fix.ClOrdID('1'))
    message.setField(fix.HandlInst('1'))
    message.setField(fix.Symbol('BMLL'))
    message.setField(fix.Side(fix.Side_BUY))
    message.setField(fix.OrdType(fix.OrdType_MARKET))
    message.setField(fix.Text("Hello Exchange! How are you?"))

    fix.Session.sendToTarget(message, sessionID)


class MyApplication(fix.Application):
    sessionID = None
    active = None

    def onCreate(self, sessionID): return
    def onLogon(self, sessionID):
        print 'Thanks logging me in, exchange!'
        self.sessionID = sessionID

    def onLogout(self, sessionID): return
    def toAdmin(self, message, sessionID):
        print 'toAdmin'
        
    def fromAdmin(self, message, sessionID):
        print 'fromAdmin'
    def toApp(self, sessionID, message): return
    def fromApp(self, sessionID, message):
        print 'fromApp'

    def run(self):
        self.active = True
        while self.active:
            print "I'm active!"
            if self.sessionID is None:
                sleep(.1)
                continue

            sendHelloWorldMessage(self.sessionID)
            self.active = False


fileName = 'trader_settings.ini'
settings = fix.SessionSettings(fileName)

app = MyApplication()

storeFactory = fix.FileStoreFactory(settings)
logFactory = fix.FileLogFactory(settings)

initiator = fix.SocketInitiator(app, storeFactory, settings, logFactory)
initiator.start()

app.run()

initiator.stop()
