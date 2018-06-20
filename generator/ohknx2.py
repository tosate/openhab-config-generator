import openhab2


class KnxItem(openhab2.Item):
    def __init__(self, item_type: str, name: str, label: str, state_presentation: str, icon: str):
        openhab2.Item.__init__(self, item_type, name, label, state_presentation, icon)
        self.channel = ''
        self.parent_thing = None

    def get_knx_thing_config(self) -> str:
        config = 'Type ' + self.item_type.lower() + ' : ' + self.name + ' "' + self.label + '" [ '\
                 + self.get_knx_parameter_config() + ' ]'
        return config

    def get_knx_parameter_config(self) -> str:
        return ''

    def set_parent_thing(self, parent: object):
        self.parent_thing = parent

    def get_channels(self) -> str:
        channel = 'channel="knx:device:bridge:' + self.parent_thing.thing_id + ':' + self.name + '"'
        return channel

    def get_binding_config(self) -> str:
        binding = '{ ' + self.get_channels() + ' }'
        return binding


class KnxThing(openhab2.Thing):
    def __init__(self, name: str, actuator_address: str):
        openhab2.Thing.__init__(self, '', 'device', name, '', '')

        self.parameters['actuator_address'] = actuator_address
        self.parameters['fetch'] = True
        self.parameters['pingInterval'] = 300
        self.parameters['readInterval'] = 3600
        self.items = []
        self.tab_level = 2

    def get_basic_config(self):
        config = '\t' * (self.tab_level-1) + self.thing_type + ' ' + self.type_id + ' ' + self.thing_id

        return config

    def get_knx_config(self):
        config = self.get_config()

        if len(self.items) > 0:
            config = config + ' {'

            for item in self.items:
                config = config + '\n' + '\t' * self.tab_level + item.get_knx_thing_config() + ','
            config = config[:len(config)-1] + '\n' + '\t' * (self.tab_level-1) + '}'

        return config

    def add_item(self, item: KnxItem):
        item.set_parent_thing(self)
        self.items.append(item)


class KnxBridge(openhab2.Thing):
    def __init__(self, ip_address: str, port_number: int, local_ip: str):
        openhab2.Thing.__init__(self, 'knx', 'ip', 'bridge', '', '')
        self.thing_type = 'Bridge'
        self.parameters['ipAddress'] = ip_address
        self.parameters['portNumber'] = port_number
        self.parameters['localIp'] = local_ip
        self.parameters['type'] = 'TUNNEL'
        self.parameters['readingPause'] = 50
        self.parameters['responseTimeout'] = 10
        self.parameters['readRetries'] = 3
        self.parameters['autoreconnectPeriod'] = 1
        self.parameters['localSourceAddress'] = '0.0.0'
        self.things = []

    def add_thing(self, thing: KnxThing):
        self.things.append(thing)

    def get_config(self):
        config = openhab2.Thing.get_config(self)

        if len(self.things) > 0:
            config = config + ' {'
            for thing in self.things:
                config = config + '\n' + '\t' * self.tab_level + thing.get_knx_thing_config() + ','
            config = config[:len(config)-1] + '\n}'

        return config


class SwitchItem(KnxItem):
    def __init__(self, name: str, label: str, icon: str, main_ga: str, listening_ga: str):
        KnxItem.__init__(self, 'Switch', name, label, '[%s]', icon)
        self.main_ga = main_ga
        self.listening_ga = listening_ga

    def get_knx_parameter_config(self) -> str:
        config = 'ga="' + self.main_ga + '+<' + self.listening_ga + '"'
        return config


class DimmerItem(KnxItem):
    def __init__(self, name: str, label: str, icon: str, main_ga: str, listening_ga: str, position_ga: str,
                 listening_position_ga: str, increase_decrease_ga: str):
        KnxItem.__init__(self, 'Dimmer', name, label, '[%d %%]', icon)
        self.main_ga = main_ga
        self.listening_ga = listening_ga
        self.position_ga = position_ga
        self.listening_position_ga = listening_position_ga
        self.increase_decrease_ga = increase_decrease_ga

    def get_knx_parameter_config(self) -> str:
        config = 'switch="' + self.main_ga + '+<' + self.listening_ga + '", position="' + self.position_ga + '+<'\
                 + self.listening_position_ga + '", increaseDecrease="' + self.increase_decrease_ga + '"'
        return config


class RollershutterItem(KnxItem):
    def __init__(self, name: str, label: str, up_down_ga: str, stop_move_ga: str, position_ga: str,
                 listening_position_ga: str):
        KnxItem.__init__(self, 'Rollershutter', name, label, '[%d %%]', openhab2.ICON_BLINDS)
        self.up_down_ga = up_down_ga
        self.stop_move_ga = stop_move_ga
        self.position_ga = position_ga
        self.listening_position_ga = listening_position_ga

    def get_knx_parameter_config(self) -> str:
        config = 'upDown="' + self.up_down_ga + '", stopMove="' + self.stop_move_ga + '", position='""\
                 + self.position_ga + '+<' + self.listening_position_ga + '"'
        return config


class ContactItem(KnxItem):
    def __init__(self, name: str, label: str, main_ga: str):
        KnxItem.__init__(self, 'Contact', name, label, '', openhab2.ICON_CONTACT)
        self.main_ga = main_ga

    def get_knx_parameter_config(self) -> str:
        config = 'ga="' + self.main_ga + '"'
        return config
