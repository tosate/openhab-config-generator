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
ICON_CLOCK = 'clock'
ICON_SUN = 'sun'
ICON_SUESET = 'sunset'
ICON_SUN_CLOUDS = 'sun_clouds'
ICON_MOON = 'moon'


class Thing:
    def __init__(self, binding_id: str, type_id: str, thing_id: str, label: str, location: str):
        self.thing_type = 'Thing'
        self.binding_id = binding_id
        self.type_id = type_id
        self.thing_id = thing_id
        self.label = label
        self.location = location
        self.parameters = {}
        self.tab_level = 1
        self.items = []

    def get_basic_config(self) -> str:
        config = '\t' * (self.tab_level-1) + self.thing_type + ' ' + self.binding_id + ':' + self.type_id + ':' + self.thing_id
        if self.label:
            config = config + ' "' + self.label + '"'

        if self.location:
            config = config + ' @ "' + self.location + '"'

        return config

    def get_config(self) -> str:
        config = self.get_basic_config()

        if len(self.parameters) > 0:
            config = config + ' ['

            for key in self.parameters.keys():
                if type(self.parameters.get(key)) is str:
                    config = config + '\n' + '\t' * self.tab_level + '{}="{}",'.format(key, self.parameters.get(key))
                elif type(self.parameters.get(key)) is bool:
                    if self.parameters.get(key):
                        value = 'true'
                    else:
                        value = 'false'
                    config = config + '\n' + '\t' * self.tab_level + '{}={},'.format(key, value)
                else:
                    config = config + '\n' + '\t' * self.tab_level + '{}={},'.format(key, self.parameters.get(key))

            config = config[:len(config)-1] + '\n' + '\t' * (self.tab_level-1) + ']'

        return config


class Item:
    def __init__(self, item_type: str, name: str, label: str, state_presentation: str, icon: str):
        self.item_type = item_type
        self.name = name
        self.label = label
        self.state_presentation = state_presentation
        self.icon = icon
        self.groups = []
        self.tags = []

    def add_tag(self, tag: str):
        self.tags.append(tag)

    def get_binding_config(self):
        return ''

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

    def get_config(self):
        config = self.item_type + ' ' + self.name + ' "' + self.label + ' ' + self.state_presentation + '" '
        if self.icon:
            config = config + '<' + self.icon + '> '

        if len(self.groups) > 0:
            config = config + '('

            for group in self.groups:
                config = config + group + ', '

            config = config[:len(config) - 2] + ') '

        if len(self.tags) > 0:
            config = config + '['

            for tag in self.tags:
                config = config + '"' + tag + '", '

            config = config[:len(config) - 2] + '] '

        config = config + self.get_binding_config()
        return config


class Group(Item):
    def __init__(self, name: str, label: str, state_presentation: str, icon: str=None, item_type: str=None,
                 func: str=None):
        Item.__init__(self, 'Group', name, label, state_presentation, icon)
        self.item_type = item_type
        self.func = func

    def get_config(self) -> str:
        group_str = 'Group'

        if self.item_type:
            group_str = group_str + ':' + self.item_type

        if self.func:
            group_str = group_str + ':' + self.func

        group_str = group_str + ' ' + self.name + ' "' + self.label + '" '

        if self.icon:
            group_str = group_str + '<' + self.icon + '> '
        group_str = self.get_group_list(group_str)
        return group_str
