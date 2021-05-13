# from util.logging import FORMAT_STRING
from logformatelement import LogFormatElement

FORMAT_STRING = '%(asctime)s | %(levelname)-8s | %(name)20s | %(funcName)15s() | %(message)s'


class LogFormat:

    def __init__(
            self,
            separator="|",
            formatstring=FORMAT_STRING
    ):
        self.separator = separator
        self.elements = []
        self.formatstring = formatstring
        # self.parsestring(self._formatstring)

    @property
    def formatstring(self):
        return self._formatstring

    @formatstring.setter
    def formatstring(self, formatstring):
        print("@formatstring.setter")
        strings = formatstring.split(self.separator)
        elements = []
        for string in strings:
            element = LogFormatElement.fromstring(string)
            elements.append(element)
        self.elements = elements
        self._formatstring = f" {self.separator} ".join(map(str, self.elements))

    def __str__(self):
        return self._formatstring

    def __repr__(self):
        return self._formatstring


if __name__ == '__main__':
    lf = LogFormat()
    print(lf)
    lf.formatstring = "%(a)-10s|%(b)2s"
    print(lf)
