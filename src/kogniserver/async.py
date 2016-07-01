import logging
import os
import signal

try:
    import asyncio
except ImportError:
    # Trollius >= 0.3 was renamed
    import trollius as asyncio

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from services import SessionHandler


class Component(ApplicationSession):

    @staticmethod
    def on_ping(event):
        logging.debug(event)

    @asyncio.coroutine
    def onJoin(self, details):
        # init members
        if os.environ.get('DEBUG') in ['1','True','true','TRUE']:
            log_level = logging.DEBUG
        else:
            log_level = logging.WARN
        logging.basicConfig()
        logging.getLogger().setLevel(log_level)
        self.session = SessionHandler(self, log_level)

        # register RPC
        reg = yield self.register(self.session.register_scope, 'service.displayserver.register')

        # setup ping
        sub = yield self.subscribe(self.on_ping, "com.wamp.ping")

        print 'kogniserver(asyncio) started...'

        # self.running = True

        # try:
        #     while self.running:
        #         logging.debug("ping")
        #         self.publish("com.wamp.ping", "ping")
        #         yield asyncio.sleep(1)
        # except Exception as e:
        #     logging.debug(e)
        #     raise e

    def onLeave(self, details):
        self.session.quit()
        print("kogniserver session left...")


def main_entry():
    from autobahn.asyncio.wamp import ApplicationRunner
    runner = ApplicationRunner(url=u"ws://127.0.0.1:8181/ws", realm=u"realm1")
    try:
        runner.run(Component)
    except KeyboardInterrupt or Exception:
        raise KeyboardInterrupt
    print "shutting down kogniserver..."

if __name__ == '__main__':
    main_entry()
