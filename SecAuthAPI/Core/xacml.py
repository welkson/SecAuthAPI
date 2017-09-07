class Util:
    @staticmethod
    def get_policy_name(content):
        from BeautifulSoup import BeautifulStoneSoup as Soup
        soup = Soup(content)
        return soup.policy["policyid"]

        # TODO: old implementation (remove)
        # from xml.dom import minidom     # TODO:
        # xmldoc = minidom.parseString(content)
        # itemlist = xmldoc.getElementsByTagName('Policy')
        # return itemlist[0].attributes['PolicyId'].value
