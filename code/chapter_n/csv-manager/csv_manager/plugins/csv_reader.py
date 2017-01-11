from groundwork.patterns import GwCommandsPattern


class csv_reader(GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("hello_world", "Prints hello world", self._hello)

    def _hello(self):
        print("Hello World. It's me, csv_reader!")
