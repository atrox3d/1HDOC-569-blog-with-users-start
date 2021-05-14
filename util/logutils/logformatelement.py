class LogFormatElement:
    def __init__(self, name, width=None):
        self.name = name
        self._width = width

    @classmethod
    def fromstring(cls, string: str):
        import re
        result = re.search(r"%\((.+)\)(-*[0-9]*)s", string)
        if not result:
            raise ValueError("invalid format, must be: %(name)[width]s")
        name, width = result.groups()
        return cls(name, width)

    @property
    def width(self):
        # print(f"return {self._width=}")
        return self._width

    @width.setter
    def width(self, width):
        # print(f"set self._width={width=}")
        self._width = width

    def __str__(self):
        return f"%({self.name}){self._width or ''}s"


if __name__ == '__main__':
    lfe = LogFormatElement("test")
    print(lfe)

    lfe.width = 5
    print(lfe.width)
    print(lfe)

    lfe.width = -18
    print(lfe.width)
    print(lfe)

    s = LogFormatElement.fromstring("%(ciao)-20s")
    print(s)
    print(s.name)
    print(s.width)
