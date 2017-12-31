# -*- coding: utf-8 -*-
import xmltodict


class XACML(object):

    @classmethod
    def loads(cls, *args, **kwargs):
        filename = kwargs.get('filename', None)
        content = kwargs.get('content', None)
        policy = Policy()

        def is_property(name):
            return name[0] == '@'

        def load_rule(items, parent):
            rule = Rule(parent=parent)
            for item, value in items.items():
                if is_property(item):
                    rule.add_property(item[1:], value)
                else:
                    rule.add_target(load_target(value, parent=rule))
            return rule

        def load_target(items, parent):

            if not issubclass(items.__class__, dict):
                if items is None:
                    items = dict()

            target = Target(parent=parent)
            for item, value in items.items():
                if is_property(item):
                    target.add_property(item[1:], value)
                elif item == 'AnyOf':
                    for v in value:
                        target.add_any_of(load_any_of(v, parent=target))
            return target

        def load_any_of(items, parent):
            any_of = AnyOf(parent=parent)

            if not issubclass(items.__class__, list):
                items = [items,]

            for item in items:
                for values in item.values():
                    if not issubclass(values.__class__, list):
                        values = [values,]
                    for value in values:
                        any_of.add_all_of(load_all_of(value, parent=any_of))
            return any_of

        def load_all_of(items, parent):
            all_of = AllOf(parent=parent)

            for item, values in items.items():
                if not issubclass(values.__class__, list):
                    values = [values,]
                for value in values:
                    match = load_match(value, parent=all_of)
                    policy.aux_matchs.append(match)
                    all_of.add_match(match)
            return all_of

        def load_match(items, parent):
            match = Match(parent=parent)

            for item, value in items.items():
                if is_property(item):
                    match.add_property(name=item[1:], value=value)
                elif item == 'AttributeValue':
                    load_attribute(match.attribute_value, value)
                elif item == 'AttributeDesignator':
                    load_attribute(match.attribute_designator, value)
            return match

        def load_attribute(attr, items):
            for item, value in items.items():
                if is_property(item):
                    attr.add_property(name=item[1:], value=value)
                else:
                    attr.value = value

        parse = None
        if filename is not None:
            with open(filename, 'r') as fd:
                parse = xmltodict.parse(fd.read())
        else:
            parse = xmltodict.parse(content)

        # Parse Policy
        for item, value in parse['Policy'].items():
            if is_property(item):
                policy.add_property(name=item[1:], value=value)
            elif item == 'Rule':
                rule = load_rule(value, parent=policy)
                policy.add_rule(rule=rule)
            else:
                policy.add_target(load_target(value, policy))
        return policy


    @classmethod
    def dumps(self, filename):
        pass


class BaseItem(object):

    def __init__(self, parent=None):
        self.name = self.__class__.__name__
        self.value = ''
        self.properties = dict()
        self.parent = parent

    def add_property(self, name, value):
        self.properties[name] = Property(name, value)

    def toXML_extra(self):
        return ''

    def is_toXML(self):
        return True

    def toXML(self):
        if self.is_toXML():
            properties = list()
            for property in self.properties.values():
                properties.append(property.toXML())
            return '<{0} {1}>{2}{3}</{0}>'.format(self.name, ' '.join(properties), self.value, self.toXML_extra())
        return ''



class Property(BaseItem):

    def __init__(self, name, value):
        super(Property, self).__init__()
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.value == other


    def toXML(self):
        return '{}="{}"'.format(self.name, self.value)


class Attribute(BaseItem):

    def __init__(self, name, value):
        super(Attribute, self).__init__()
        self.name = name
        self.value = value
        self.properties = dict()

    def __getitem__(self, item):
        return self.properties[item]


class Policy(BaseItem):

    def __init__(self):
        super(Policy, self).__init__()
        self.properties = dict()
        self.targets = list()
        self.rules = list()

        # Aux Lists
        self.aux_matchs = list()

    def add_target(self, target):
        self.targets.append(target)

    def add_rule(self, rule):
        self.rules.append(rule)

    def remove_any_of_by_name(self, name):
        match = self.get_match_by_value(name)

        all_of = match.parent
        any_of = all_of.parent

        any_of.all_ofs.remove(all_of)

    def get_match_by_value(self, value):
        for match in self.aux_matchs:
            if match.attribute_designator['AttributeId'] == value:
                return match
        return None

    def is_toXML(self):
        return len(self.targets) > 0 or len(self.rules) > 0

    def toXML_extra(self):
        targets = list()
        for target in self.targets:
            targets.append(target.toXML())

        rules = list()
        for rule in self.rules:
            rules.append(rule.toXML())

        return '{}\n{}'.format(
            '\n'.join(targets),
            '\n'.join(rules)
        )


class Rule(BaseItem):

    def __init__(self, parent):
        super(Rule, self).__init__(parent)
        self.properties = dict()
        self.targets = list()

    def add_target(self, target):
        self.targets.append(target)

    def is_toXML(self):
        return len(self.targets) > 0

    def toXML_extra(self):
        targets = list()
        for target in self.targets:
            targets.append(target.toXML())

        return '{}'.format(
            '\n'.join(targets),
        )


class Target(BaseItem):

    def __init__(self, parent):
        super(Target, self).__init__(parent)
        self.properties = dict()
        self.any_ofs = list()

    def add_any_of(self, any_of):
        self.any_ofs.append(any_of)

    def is_toXML(self):
        return len(self.any_ofs) > 0 or self.parent.__class__ == Policy

    def toXML_extra(self):
        any_ofs = list()
        for any_of in self.any_ofs:
            any_ofs.append(any_of.toXML())

        return '{}'.format(
            '\n'.join(any_ofs)
        )


class AnyOf(BaseItem):

    def __init__(self, parent):
        super(AnyOf, self).__init__(parent)
        self.properties = dict()
        self.all_ofs = list()

    def add_all_of(self, all_of):
        self.all_ofs.append(all_of)

    def is_toXML(self):
        return len(self.all_ofs) > 0

    def toXML_extra(self):
        all_ofs = list()
        for all_of in self.all_ofs:
            all_ofs.append(all_of.toXML())

        return '{}'.format(
            '\n'.join(all_ofs)
        )


class AllOf(BaseItem):

    def __init__(self, parent):
        super(AllOf, self).__init__(parent)
        self.properties = dict()
        self.matchs = list()

    def add_match(self, match):
        self.matchs.append(match)

    def is_toXML(self):
        return len(self.matchs) > 0

    def toXML_extra(self):
        matchs = list()
        for match in self.matchs:
            matchs.append(match.toXML())

        return '{}'.format(
            '\n'.join(matchs)
        )


class Match(BaseItem):

    def __init__(self, parent):
        super(Match, self).__init__(parent)
        self.properties = dict()
        self.attribute_value = Attribute(name='AttributeValue', value='')
        self.attribute_designator = Attribute(name='AttributeDesignator', value='')

    def toXML(self):
        properties = list()
        for property in self.properties.values():
            properties.append(property.toXML())

        return '<{0} {1}>\n\t{2}\n\t{3}\t\n</{0}>'.format(
            self.name,
            ' '.join(properties),
            self.attribute_value.toXML(),
            self.attribute_designator.toXML()
        )
