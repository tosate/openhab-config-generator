import openhab2


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
                config = config + '\n' + thing.get_config() + ','
            config = config[:len(config)-1] + '\n}'

        return config


class KnxItem(openhab2.Item):
    def __init__(self, item_type: str, name: str, label: str, state_presentation: str, icon: str):
        openhab2.Item(self, item_type, name, label, state_presentation, icon)
        self.channel


class SwitchItem(KnxItem):
    def __init__(self, name: str, label: str, icon: str):
        KnxItem(self, 'switch', name, label, '[%s]', icon)


class DimmerItem(KnxItem):
    def __init__(self, name: str, label: str, icon: str):
        KnxItem(self, 'dimmer', name, label, '[%d %%]', icon)


class RollershutterItem(KnxItem):
    def __init__(self, name: str, label: str):
        KnxItem(self, 'rollershutter', name, label, '[%d %%]', openhab2.ICON_BLINDS)


class ContactItem(KnxItem):
    def __init__(self, name: str, label: str):
        KnxItem(self, 'contact', name, label, '', openhab2.ICON_CONTACT)
