# -*- coding: utf-8 -*-

from lxml import etree
from collections import OrderedDict
import xmltodict
import json
import sys
from BeautifulSoup import BeautifulStoneSoup as Soup
from functools import reduce
from SecAuthAPI.Core.GenerateDS_XACML import xacml_wd17 as gds_xacml
from StringIO import StringIO   # TODO: py3 -> from io import StringIO
import operator


def get_from_dict(data_dict, keys):
    return reduce(operator.getitem, keys, data_dict)


def set_in_dict(data_dict, keys, value):
    get_from_dict(data_dict, keys[:-1])[keys[-1]] = value


def gen_xacml_add_attribute(category, attribute_id, attribute_value):
    attr_template = """<AnyOf>
        <AllOf>
            <Match MatchId="urn:oasis:names:tc:xacml:1.0:function:string-equal">
                <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">%s</AttributeValue>
                <AttributeDesignator Category="%s" AttributeId="%s" DataType="http://www.w3.org/2001/XMLSchema#string" MustBePresent="true"></AttributeDesignator>
            </Match>
        </AllOf>
    </AnyOf>""" % (attribute_value, category, attribute_id)

    return attr_template


class Xacml:
    @staticmethod
    def get_policy_name(content):
        soup = Soup(content)
        return soup.policy["policyid"]

    @staticmethod
    def get_rule_index(policy_dic, rule_name):
        if type(policy_dic.get('Policy').get('Rule')) == list:  # if Lists then N rules
            for n, r in enumerate(policy_dic.get('Policy').get('Rule')):
                if r['@RuleId'] == rule_name:
                    return n
        return -1   # only 1 rule

    @staticmethod
    def get_attribute(policy_dic, rule_idx, attribute_id):
        if rule_idx >= 0:
            if type(policy_dic.get('Policy').get('Rule')[rule_idx].get('Target').get('AnyOf')) == list:  # multiples attributes? (List)
                for attr in policy_dic.get('Policy').get('Rule')[rule_idx].get('Target').get('AnyOf'):
                    if attr.get('AllOf').get('Match').get('AttributeDesignator').get('@AttributeId') == attribute_id:
                        return attr
            else:   # only 1 attribute (no List)
                if policy_dic.get('Policy').get('Rule')[rule_idx].get('Target').get('AnyOf').get('AllOf').get('Match').get('AttributeDesignator').get('@AttributeId') == attribute_id:
                    return policy_dic.get('Policy').get('Rule')[rule_idx].get('Target').get('AnyOf')

        else:  # only 1 rule (no List)
            if type(policy_dic.get('Policy').get('Rule').get('Target').get('AnyOf')) == list:  # multiples attributes? (List)
                for attr in policy_dic.get('Policy').get('Rule').get('Target').get('AnyOf'):
                    if attr.get('AllOf').get('Match').get('AttributeDesignator').get('@AttributeId') == attribute_id:
                        return attr
            else:  # only 1 attribute (no List)
                if policy_dic.get('Policy').get('Rule').get('Target').get('AnyOf').get('AllOf').get('Match').get('AttributeDesignator').get('@AttributeId') == attribute_id:
                    return policy_dic.get('Policy').get('Rule').get('Target').get('AnyOf')
        return None  # attribute not found

    @staticmethod
    def validate_policy(policy):
        # validating XACML from XSD
        schema = etree.XMLSchema(file='xacml-core-v3-schema-wd-17.xsd')  # TODO: fix path (extra folder?)
        xml_doc = etree.fromstring(policy)
        if schema.validate(xml_doc):
            return {'IsValid': True}, {'message': 'Policy is Valid!'}
        else:
            return {'IsValid': False}, {'message': schema.error_log}

    @staticmethod
    def modify_attribute(policy, rule_name, attribute_name, attribute_value):
        # convert xacml to Dict
        policy_dic = xmltodict.parse(policy)

        # get rule index
        rule_idx = Xacml.get_rule_index(policy_dic, rule_name)

        # get attribute in rule
        attr = Xacml.get_attribute(policy_dic, rule_idx, attribute_name)
        if attr:
            attr.get('AllOf').get('Match').get('AttributeValue')['#text'] = attribute_value  # change attribute

        # convert from dict to xacml and return the policy
        return xmltodict.unparse(policy_dic, full_document=False, pretty=True, depth=0, indent="    ")

    @staticmethod
    def add_atribute(policy, rule_name, category_id, attribute_name, attribute_value):
        # policy model from string
        p = gds_xacml.parseString(policy, silence=True)

        # generate attribute xml string
        new_attr_str = gen_xacml_add_attribute(category_id, attribute_name, attribute_value)

        # generate xml/xacml object from string
        new_attribute = gds_xacml.parseString(new_attr_str, silence=True)

        # get Rule tag
        r1 = p.get_Rule()[0]    # TODO: retrive rule from rule_name

        # get Target from Rule
        t1 = r1.get_Target()

        # add new attribute
        t1.add_AnyOf(new_attribute)

        # export xacml model to string
        try:
            old_stdout = sys.stdout
            result = StringIO()
            sys.stdout = result
            p.export(sys.stdout, 0, namespace_='')

        finally:
            sys.stdout = old_stdout

        return result.getvalue()
