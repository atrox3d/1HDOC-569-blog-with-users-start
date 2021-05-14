# from util.logging import FORMAT_STRING
try:
    from logformatelement import LogFormatElement
except ImportError:
    from .logformatelement import LogFormatElement


FORMAT_STRING = '%(asctime)s | %(levelname)-8s | %(name)20s | %(funcName)15s() | %(message)s'


class LogFormat:

    def __init__(
            self,
            formatstring=FORMAT_STRING,
            separator=" | ",
    ):
        self._formatstring = ""
        self.separator = separator
        self.elements = dict()
        self.formatstring = formatstring
        # self.parsestring(self._formatstring)

    @property
    def formatstring(self):
        return self._formatstring

    @formatstring.setter
    def formatstring(self, formatstring):
        strings = formatstring.split(self.separator)
        elements = {}

        for string in strings:
            element = LogFormatElement.fromstring(string)
            elements[element.name] = element

        self.elements.clear()
        self.elements.update(elements)
        self.update()

    def update(self):
        self._formatstring = self.separator.join(map(str, self.elements.values()))

    def __str__(self):
        return self._formatstring

    def __repr__(self):
        return self._formatstring

    def setwidth(self, name, width):
        if isinstance(name, int):
            keys = list(self.elements.keys())
            print(keys)
            name = keys[name]
        element: LogFormatElement = self.elements.get(name)
        if not element:
            raise IndexError(f"element {name} not found")
        element.width = width
        self.update()


if __name__ == '__main__':
    lf = LogFormat()
    print(lf)
    lf.formatstring = "%(a)-10s|%(b)2s"
    print(lf)
    lf.setwidth('a', 20)
    print(lf)
