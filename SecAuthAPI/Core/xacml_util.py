# -*- coding: utf-8 -*-

from lxml import etree
import xml.dom.minidom
from ModelMapper import *


class XacmlUtil:

    def __init__(self, content):
        self.content = content
        self.policy = XACML.loads(content=self.content)

    def get_policy_name(self):
        return self.policy.properties.get('PolicyId').value

    def validate_policy(self):
        # validating XACML from XSD
        schema = etree.XMLSchema(file='xacml-core-v3-schema-wd-17.xsd')       # TODO: fix path (extra folder?)
        xml_doc = etree.fromstring(self.content)
        if schema.validate(xml_doc):
            return {'IsValid': True}, {'message': 'Policy is Valid!'}
        else:
            return {'IsValid': False}, {'message': schema.error_log}

    def add_atribute(self, rule_name, category_id, attribute_name, attribute_value):
        # get attribute from target
        target = self.policy.rules[0].targets[0]                              # TODO: use rule_name

        anyof = AnyOf(parent=target)
        allof = AllOf(parent=anyof)

        # define properties to new attribute
        match = Match(parent=allof)
        match.add_property(name='MatchId', value='urn:oasis:names:tc:xacml:1.0:function:string-equal')
        match.attribute_value.value = attribute_value
        match.attribute_value.add_property(name='DataType', value='http://www.w3.org/2001/XMLSchema#string')

        # define type and category
        match.attribute_designator.add_property(name='AttributeId',
                                                value=attribute_name)
        match.attribute_designator.add_property(name='Category',
                                                value=category_id)
        match.attribute_designator.add_property(name='DataType', value='http://www.w3.org/2001/XMLSchema#string')
        match.attribute_designator.add_property(name='MustBePresent', value='true')

        # add new attribute
        allof.add_match(match=match)
        anyof.add_all_of(all_of=allof)
        target.add_any_of(any_of=anyof)

        return self.policy

    def modify_attribute(self, rule_name, attribute_name, attribute_value):   # TODO: use rule_name
        atributo = self.policy.get_match_by_value(attribute_name)
        atributo.attribute_value.value = attribute_value

        return self.policy

    def remove_attribute(self, rule_name, attribute_name):                    # TODO: use rule_name
        self.policy.remove_any_of_by_name(attribute_name)

        return self.policy

    def xacml_formatter(self):
        return xml.dom.minidom.parseString(self.content).toprettyxml()
