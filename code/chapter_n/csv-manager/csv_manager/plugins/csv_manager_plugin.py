from groundwork.patterns import GwCommandsPattern
import threading
import time


class csv_manager_plugin(GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("hello_world", "Prints hello world", self._hello)
        self.signals.register("test_signal", "blablabla")

        self.signals.connect(receiver="my_test_receiver",
                             signal="test_signal",
                             function=self._signal_hello,
                             description="Blub")

        test_thread = TestThread(self)
        test_thread.start()
        time.sleep(5)

    def _hello(self):
        print("Hello World. It's me, csv_manager_plugin!")

    def _signal_hello(self, plugin, **kwargs):
        print("Got signal from %s with %s" % (plugin.name, kwargs.get("data", None)))


class TestThread(threading.Thread):
    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin
        self.app = plugin.app

    def run(self):
        i = 0
        while i < 1:
            print("jupp %s" % i)
            # self.plugin.signals.send("test_signal", data="DATA %s" % i)
            self.plugin.signals.send("test_signal", data="test")
            time.sleep(1)
            i += 1
