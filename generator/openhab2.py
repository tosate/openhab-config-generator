from _ctypes import sizeof

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

