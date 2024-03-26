from hvlp.client import HvlpClient

import threading
from hvlp.errors import HvlpError

BROKER_ADDR = 'localhost'
BROKER_PORT = 65432
N = 10000

class TestCase(object):

    def __init__(self):

        # Create the clients
        self.producer = HvlpClient(srv_addr=BROKER_ADDR, port=BROKER_PORT)
        self.consumer = HvlpClient(srv_addr=BROKER_ADDR, port=BROKER_PORT)
        self.stop_event = threading.Event()


class HVLP_NET_01_01_01(TestCase):


    def __init__(self):
        super(HVLP_NET_01_01_01, self).__init__()
        self.tag = self.__class__.__name__
        self.description = ("Send a burst of connect messages to the broker and check if the broker is able to handle "
                            "the load.")

    def execute(self):

        # Open the sockets
        self.producer.open()
        self.consumer.open()

        for i in range(N):
            self.producer.connect()
            self.consumer.connect()

        # Check that the broker is able to handle the load
        self.producer.disconnect()
        self.consumer.disconnect()

class HVLP_NET_01_01_02(TestCase):

    def __init__(self):
        super(HVLP_NET_01_01_02, self).__init__()
        self.tag = self.__class__.__name__
        self.description = ("Send a burst of disconnect messages to the broker and check if the broker is able to "
                            "handle the load.")

    def execute(self):

        # Open the sockets
        self.producer.open()
        self.consumer.open()

        for i in range(N):
            self.producer.connect()
            self.consumer.connect()

        # If the server is broker, we will know it here
        self.producer.disconnect()
        self.consumer.disconnect()


class HVLP_NET_01_01_03(TestCase):

    def __init__(self):
        super(HVLP_NET_01_01_03, self).__init__()
        self.tag = self.__class__.__name__
        self.description = ("Cycle connect and disconnect messages to the broker and check if the broker is able to "
                            "handle to the load.")

    def execute(self):

        try:
            # Open the sockets
            self.producer.open()

            for i in range(N):
                try:
                    self.producer.connect()
                    self.producer.disconnect()
                except HvlpError:
                    print(i)
                    break

        except Exception:
            raise


class HVLP_NET_01_01_04(TestCase):

        def __init__(self):
            super(HVLP_NET_01_01_04, self).__init__()
            self.tag = self.__class__.__name__
            self.description = ("Send a burst of subscribe messages to the broker and check if the broker is able to "
                                "handle the load.")

        def execute(self):

            # Open the sockets
            self.producer.open()
            self.consumer.open()

            # Connect the clients
            self.producer.connect()

            for i in range(N):
                self.producer.subscribe(str(i))

            # If the server is broker, we will know it here
            self.producer.disconnect()

class HVLP_NET_01_01_05(TestCase):

    def __init__(self):
        super(HVLP_NET_01_01_05, self).__init__()
        self.tag = self.__class__.__name__
        self.description = ("Send a burst of unsubscribe messages to the broker and check if the broker is able to "
                            "handle the load.")

    def execute(self):

        # Open the sockets
        self.producer.open()
        self.consumer.open()

        # Connect the clients
        self.producer.connect()

        for i in range(N):
            self.producer.unsubscribe(str(i))

        # If the server is broker, we will know it here
        self.producer.disconnect()


class HVLP_NET_01_01_06(TestCase):

    def __init__(self):
        super(HVLP_NET_01_01_06, self).__init__()
        self.tag = self.__class__.__name__
        self.description = ("Cycle subscribe and unsubscribe messages to the broker and check if the broker is able to "
                            "handle the load.")

    def execute(self):

        # Open the sockets
        self.producer.open()
        self.consumer.open()

        # Connect the clients
        self.producer.connect()
        self.consumer.connect()

        for i in range(N):
            self.producer.subscribe(str(i))
            self.consumer.subscribe(str(i))
            self.producer.unsubscribe(str(i))
            self.consumer.unsubscribe(str(i))

        # If the server is broker, we will know it here
        self.producer.disconnect()
        self.consumer.disconnect()

class HVLP_NET_01_01_07(TestCase):

    def __init__(self):
        super(HVLP_NET_01_01_07, self).__init__()
        self.tag = self.__class__.__name__
        self.description = ("Send a burst of publish messages to the broker and check if the broker is able to "
                            "handle the load.")


    def execute(self):

            # Open the sockets
            self.producer.open()

            # Connect the clients
            self.producer.connect()
            self.producer.subscribe('test')

            for i in range(N):
                self.producer.publish('test', 1)

            # If the server is broker, we will know it here
            self.producer.unsubscribe('test')
            self.producer.disconnect()

tests = (
    HVLP_NET_01_01_01(),
    HVLP_NET_01_01_02(),
    HVLP_NET_01_01_03(),
    HVLP_NET_01_01_04(),
    HVLP_NET_01_01_05(),
    HVLP_NET_01_01_06(),
    HVLP_NET_01_01_07(),
)

for test in tests:
    test.execute()
    print("Test {test} completed successfully.".format(test=test))