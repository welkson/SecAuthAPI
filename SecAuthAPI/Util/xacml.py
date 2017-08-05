class Util:
    @staticmethod
    def get_policy_name(content):
        from xml.dom import minidom
        xmldoc = minidom.parseString(content)
        itemlist = xmldoc.getElementsByTagName('Policy')
        return itemlist[0].attributes['PolicyId'].value
