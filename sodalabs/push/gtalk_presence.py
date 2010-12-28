import sys, time
import sleekxmpp

class PresenceBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, presence):
        try:
            domain = jid.split('@')[1]
        except IndexError:
            jid = '%s@gmail.com' % jid

        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.registerPlugin('xep_0030') # Service Discover
        self.registerPlugin('xep_0004') # Data forms
        self.registerPlugin('xep_0060') # PubSub
        self.registerPlugin('xep_0199') # XMPP Ping

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('sent_prsence', self.sent_presence)

        self.presence = presence
        
        if self.connect(('talk.google.com', 5222)):
            self.process(threaded=True)
            print 'Done'
        else:
            print 'Unable to connect'

    def start(self, event):
        #self.getRoster()
        self.sendPresence(pstatus=self.presence)

    def sent_presence(self, event):
        self.disconnect()
