# -*- coding: utf-8 -*-

from lxml import etree
from collections import OrderedDict
import xmltodict
import json
from BeautifulSoup import BeautifulStoneSoup as Soup
from functools import reduce
import operator


def get_from_dict(data_dict, keys):
    return reduce(operator.getitem, keys, data_dict)


def set_in_dict(data_dict, keys, value):
    get_from_dict(data_dict, keys[:-1])[keys[-1]] = value


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
    def add_attribute(policy, rule_name, category_id, attribute_name, attribute_value):
        pass
