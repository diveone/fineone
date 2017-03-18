from xmltodict import parse as xmlparser, ParsingInterrupted


class XmlParser(object):

    def parse(self, xml_input, encoding=None, force_list=None, postprocessor=None):
        """
        Parse xml document into a Python dictionary.

        :param xml_input: `xml`, xml document
        :param encoding: string encoding
        :param force_list: `list`, a list or tuple with names of keys to force into a list
        :param postprocessor: `function`, used when more complex logic required for keys and values
        :return: `dict`, xml data transformed into a dictionary
        """
        try:
            xmlparser(stream, item_depth=2, item_callback=self.validate)
        except ParsingInterrupted as exc:
            raise exc
        else:
            xmlparser(stream, encoding=encoding, force_list=force_list, postprocessor=None)

    def validate(self, path, item):
        """
        Before parsing the full xml, check api response.
        :param path: xml parent elements of the item
        :param item: xml elements at the path
        :return: `bool`, status of xml response validity
        :raise: `ParsingInterrupted` if `False`
        """
        response = dict(item)
        if not response.get('errorNum') == 0:
            return False
