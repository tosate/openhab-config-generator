import operator

ICON_HOUSE = 'house'
ICON_LIGHT = 'light'
ICON_GROUNDFLOOR = 'groundfloor'
ICON_FIRSTFLOOR = 'firstfloor'
ICON_GARAGE = 'garage'
ICON_KITCHEN = 'kitchen'
ICON_LIVING_ROOM = 'sofa'
ICON_BEDROOM = 'bedroom'
ICON_OFFICE = 'office'
ICON_BATH = 'bath'
ICON_CORRIDOR = 'corridor'
ICON_TOILET = 'toilet'
ICON_WASHINGMACHINE = 'washingmachine'
ICON_GROUP = 'group'
ICON_BOY = 'boy_3'
ICON_GIRL = 'girl_3'
ICON_BLINDS = 'blinds'
ICON_CONTACT = 'contact'
ICON_POWER_OUTLET = 'poweroutlet'


class OHObject:
    DPT1_Switch = '1.001'
    DPT1_Up_Down = '1.008'
    DPT1_Stop = '1.007'
    DPT1_Trigger = '1.017'  # not supported
    DPT3_Dimmer_Step = '3.007'
    DPT5_Percent = '5.001'
    DPT9_Temperature_C = '9.001'

    def __init__(self, icon: str):
        self.groups = []
        self.icon = icon

    def add_group(self, group):
        self.groups.append(group)

    def get_group_list(self, item_str: str) -> str:
        if len(self.groups) > 0:
            item_str = item_str + '('
            group_names = map(operator.attrgetter('name'), self.groups)
            separator = ', '
            item_str = item_str + separator.join(group_names)

            item_str = item_str + ') '
        return item_str


class Item(OHObject):
    def __init__(self, name: str, label: str, state_presentation: str, icon: str, ga1: str=None, ga2: str=None,
                 ga3: str=None, ga4: str=None, ga5: str=None, ga6: str=None):
        OHObject.__init__(self, icon)
        self.name = name
        self.state_presentation = state_presentation
        self.label = label
        self.ga1 = ga1
        self.ga2 = ga2
        self.ga3 = ga3
        self.ga4 = ga4
        self.ga5 = ga5
        self.ga6 = ga6
        self.groups = []
        self.type = 'Unknown'

    def get_basic_item_config(self) -> str:
        if not self.state_presentation:
            item_str = self.type + ' ' + self.name + ' "' + self.label + '" '
        else:
            item_str = self.type + ' ' + self.name + ' "' + self.label + ' ' + self.state_presentation + '" '
        item_str = self.get_group_list(item_str)
        return item_str


class Group(Item):
    def __init__(self, name: str, label: str, icon: str=None):
        Item.__init__(self, name, label, '', icon)
        self.name = name
        self.label = label
        if not icon:
            self.icon = ICON_GROUP

    def get_config(self) -> str:
        group_str = 'Group ' + self.name + ' "' + self.label + '" '
        group_str = self.get_group_list(group_str)
        return group_str


class LightbulbItem(Item):
    def __init__(self, name: str, label: str, icon: str, ga1: str, ga2: str):
        Item.__init__(self, name, label, '[%s]', icon, ga1, ga2)
        self.type = 'Switch'

    # Switch GF_Office_Light "Büro EG" (GF_Office, Lights) { knx = "1/1/24+1/4/24" }
    def get_config(self) -> str:
        item_str = self.get_basic_item_config()
        # <mainGA>+<listeningGA>
        item_str = item_str + '{ knx="' + OHObject.DPT1_Switch + ':' + self.ga1 + "+" + self.ga2 + '" }'
        return item_str

    def get_sitemap_elements(self) -> list:
        result = []
        switch_element = SitemapSwitchElement(self)
        result.append(switch_element)
        return result


class ContactSensorItem(Item):
    def __init__(self, name: str, label: str, icon: str, ga1: str):
        Item.__init__(self, name, label, '', icon, ga1)
        self.type = 'Contact'

    def get_config(self) -> str:
        item_str = self.get_basic_item_config()
        item_str = item_str + '{ knx="' + self.ga1 + '" }'
        return item_str

    def get_sitemap_elements(self) -> list:
        result = []
        text_element = SitemapTextElement(self)
        result.append(text_element)
        return result


class RollershutterItem(Item):
    def __init__(self, name: str, label: str, icon: str, ga1: str, ga2: str, ga3: str, ga4: str):
        Item.__init__(self, name, label, '[%d %%]', icon, ga1, ga2, ga3, ga4)
        self.type = 'Rollershutter'

    def get_config(self) -> str:
        item_str = self.get_basic_item_config()
        # Up/Down, Stop/Move, Position+listeningPosition
        item_str = item_str + '{ knx="' + OHObject.DPT1_Up_Down + ':' + self.ga1 + ', '
        item_str = item_str + self.ga2 + ', '
        item_str = item_str + OHObject.DPT5_Percent + ':' + self.ga3 + '+<' + self.ga4 + '" }'
        return item_str

    def get_sitemap_elements(self) -> list:
        result = []
        slider = SitemapSliderElement(self)
        result.append(slider)
        return result


class JalousieItem(Item):
    def __init__(self, name: str, label: str, icon: str, ga1: str, ga2: str, ga3: str, ga4: str, ga5: str, ga6: str):
        Item.__init__(self, name, label, '[%d %%]', icon, ga1, ga2, ga3, ga4, ga5, ga6)
        self.type = 'Rollershutter'
        self.lamelle = LamelleItem(self.name + '_Lamelle', self.label + ' Lamelle', self.icon, self.ga1, self.ga2,
                                   self.ga5, self.ga6)

    def get_config(self) -> str:
        item_str = self.type + ' ' + self.name + ' "' + self.label + ' Jalousie ' + self.state_presentation + '" '
        item_str = self.get_group_list(item_str)
        # Up/Down, Stop/Move, Position_Jalousie+listeningPosition_Jalousie
        item_str = item_str + '{ knx="' + OHObject.DPT1_Up_Down + ':' + self.ga1 + ', '
        item_str = item_str + self.ga2 + ', '
        item_str = item_str + OHObject.DPT5_Percent + ':' + self.ga3 + '+<' + self.ga4 + '" }\n'

        self.lamelle.groups = self.groups
        item_str = item_str + self.lamelle.get_config()

        return item_str

    def get_sitemap_elements(self) -> list:
        result = []
        slider_jalousie = SitemapSliderElement(self)
        result.append(slider_jalousie)
        slider_lamelle = SitemapSliderElement(self.lamelle)
        result.append(slider_lamelle)
        return result


class LamelleItem(Item):
    def __init__(self, name: str, label: str, icon: str, ga1: str, ga2: str, ga3: str, ga4: str):
        Item.__init__(self, name, label, '[%d %%]', icon, ga1, ga2, ga3, ga4)
        self.type = 'Rollershutter'

    def get_config(self) -> str:
        item_str = self.type + ' ' + self.name + ' "' + self.label + ' ' + self.state_presentation +\
                   '" '
        item_str = self.get_group_list(item_str)
        # Up/Down, Stop/Move, Position_Slat+listeningPosition_Slat
        item_str = item_str + '{ knx="' + OHObject.DPT1_Up_Down + ':' + self.ga1 + ', '
        item_str = item_str + self.ga2 + ', '
        item_str = item_str + OHObject.DPT5_Percent + ':' + self.ga3 + '+<' + self.ga4 + '" }'
        return item_str


class NumberItem(Item):
    def __init__(self, name: str, label: str, icon: str, ga1: str):
        Item.__init__(self, name, label, '[%d %%]', icon, ga1)
        self.type = 'Number'

    def get_config(self) -> str:
        item_str = self.get_basic_item_config()
        item_str = item_str + '{ knx="' + OHObject.DPT5_Percent + ':' + self.ga1 + '"}'
        return item_str


class SitemapElement:
    def __init__(self, group: Group):
        self.item = None
        self.label = group.label
        self.state_presentation = None
        self.icon = group.icon
        self.type = 'Group'
        self.block = None

    def __init__(self, item: Item, label: str, state_presentation: str=None, icon: str = None):
        self.item = item
        self.label = label
        self.state_presentation = state_presentation
        self.icon = icon
        self.type = 'Unknown'
        self.block = []

    def add_element(self, element):
        self.block.append(element)

    def get_config(self) -> str:
        element_str = '\t\t' + self.type + ' item=' + self.item.name + ' label="' + self.label

        if self.state_presentation:
            element_str = element_str + ' ' + self.state_presentation

        element_str = element_str + '"'

        if self.icon:
                element_str = element_str + ' icon="' + self.icon + '"'

        if len(self.block) > 0:
            element_str = element_str + ' {\n'

            for element in self.block:
                element_str = element_str + '\t' + element.get_config() + '\n'

            element_str = element_str + '\t\t}\n'

        return element_str


class Frame:
    def __init__(self, label: str):
        self.label = label
        self.sitemap_elements = []

    def add_sitemap_element(self, element: SitemapElement):
        self.sitemap_elements.append(element)

    def get_config(self) -> str:
        frame_str = '\tFrame label="' + self.label + '" {\n'

        for element in self.sitemap_elements:
            frame_str = frame_str + element.get_config()

        frame_str = frame_str + '\t}\n'

        return frame_str


class SitemapTextElement(SitemapElement):
    def __init__(self, item: Item):
        SitemapElement.__init__(self, item, item.label, item.state_presentation, item.icon)
        self.type = 'Text'


class SitemapSwitchElement(SitemapElement):
    def __init__(self, item: Item):
        SitemapElement.__init__(self, item, item.label, item.state_presentation, item.icon)
        self.type = 'Switch'


class SitemapSliderElement(SitemapElement):
    def __init__(self, item: Item):
        SitemapElement.__init__(self, item, item.label, item.state_presentation, item.icon)
        self.type = 'Slider'
