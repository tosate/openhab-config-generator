import csv

import openhab2
import ohknx2

COL_ACTUATOR_NAME = 'Actuator_name'
COL_ACTUATOR_LABEL = 'Actuator_label'
COL_ACTUATOR_ADDRESS = 'actuator_address'
COL_CHANNEL_NAME = 'Channel_name'
COL_IN_OUT = 'In_Out'
COL_TYPE = 'type'
COL_GA1 = 'ga1'
COL_GA2 = 'ga2'
COL_GA3 = 'ga3'
COL_GA4 = 'ga4'
COL_GA5 = 'ga5'
COL_GA6 = 'ga6'

COL_NAME = 'name'
COL_LABEL = 'label'
COL_FLOOR = 'floor'
COL_ROOM_NAME = 'room_name'
COL_ROOM_LABEL = 'room_label'

FRAME_ALL_ROOMS = 'ALL_ROOMS'
FRAME_ACTIVE_LIGHTS = 'ACTIVE_LIGHTS'
FRAME_OPEN_ROLLERSHUTTERS = 'OPEN_ROLLERSHUTTERS'
FRAME_SPECIAL_FUNCTIONS = 'SPECIAL_FUNCTIONS'

SWITCH_NAME_DYNAMIC_LIGHTS = 'Lights'
SWITCH_LABEL_DYNAMIC_LIGHTS = 'Eingeschaltete Lampen'
SWITCH_NAME_DISABLE_OPEN_BLINDS = 'Disable_Open_Rollershutters'
SWITCH_LABEL_DISABLE_OPEN_BLINDS = 'Rolläden nicht öffnen'


class KnxThingsConfigBuilder:
    def __init__(self, csv_reader: csv.DictReader):
        self.csv_reader = csv_reader
        self.bridge = ohknx2.KnxBridge('127.0.0.1', 3671, '192.168.178.31')
        self.device_things = {}

    def process_csv_input(self):
        for row in self.csv_reader:
            if row[COL_TYPE] == 'Lightbulb':
                self.process_lightbulb(row)
            elif row[COL_TYPE] == 'Dimmer':
                self.process_dimmer(row)
            elif row[COL_TYPE] == 'ContactSensor':
                self.process_contact_sensor(row)
            elif row[COL_TYPE] == 'Rollershutter':
                self.process_rollershutter(row)
            elif row[COL_TYPE] == 'Jalousie':
                self.process_jalousie(row)
            elif row[COL_TYPE] == 'PowerOutlet':
                self.process_poweroutlet(row)

    def get_knx_device_thing(self, actuator_name: str, actuator_label: str, actuator_address: str) -> ohknx2.KnxThing:
        if actuator_name in self.device_things:
            return self.device_things[actuator_name]
        else:
            device_thing = ohknx2.KnxThing(actuator_name, actuator_label, actuator_address)
            self.device_things[actuator_name] = device_thing
            self.bridge.add_thing(device_thing)
            return device_thing

    def process_lightbulb(self, row: dict):
        device_thing = self.get_knx_device_thing(row[COL_ACTUATOR_NAME], row[COL_ACTUATOR_LABEL],
                                                 row[COL_ACTUATOR_ADDRESS])
        channel_type_label = 'Channel ' + row[COL_IN_OUT]
        switch_channel_type = ohknx2.KnxSwitchChannelType(row[COL_CHANNEL_NAME], channel_type_label, row[COL_GA1],
                                                          row[COL_GA2])
        device_thing.add_channel_type(switch_channel_type)

    def process_dimmer(self, row: dict):
        device_thing = self.get_knx_device_thing(row[COL_ACTUATOR_NAME], row[COL_ACTUATOR_LABEL],
                                                 row[COL_ACTUATOR_ADDRESS])
        channel_type_label = 'Channel ' + row[COL_IN_OUT]
        dimmer_channel_type = ohknx2.KnxDimmerChannelType(row[COL_CHANNEL_NAME], channel_type_label, row[COL_GA1],
                                                          row[COL_GA2], row[COL_GA3], row[COL_GA4], row[COL_GA5])
        device_thing.add_channel_type(dimmer_channel_type)

    def process_contact_sensor(self, row: dict):
        device_thing = self.get_knx_device_thing(row[COL_ACTUATOR_NAME], row[COL_ACTUATOR_LABEL],
                                                 row[COL_ACTUATOR_ADDRESS])
        channel_type_label = 'Channel ' + row[COL_IN_OUT]
        contact_channel_type = ohknx2.KnxContactChannelType(row[COL_CHANNEL_NAME], channel_type_label, row[COL_GA1])
        device_thing.add_channel_type(contact_channel_type)

    def process_rollershutter(self, row: dict):
        device_thing = self.get_knx_device_thing(row[COL_ACTUATOR_NAME], row[COL_ACTUATOR_LABEL],
                                                 row[COL_ACTUATOR_ADDRESS])
        channel_type_label = 'Channel ' + row[COL_IN_OUT]
        rollershutter_channel_type = ohknx2.KnxRollershutterChannelType(row[COL_CHANNEL_NAME], channel_type_label,
                                                                        row[COL_GA1], row[COL_GA2], row[COL_GA3],
                                                                        row[COL_GA4])
        device_thing.add_channel_type(rollershutter_channel_type)

    def process_jalousie(self, row: dict):
        self.process_rollershutter(row)
        # add Lamelle
        device_thing = self.get_knx_device_thing(row[COL_ACTUATOR_NAME], row[COL_ACTUATOR_LABEL],
                                                 row[COL_ACTUATOR_ADDRESS])
        channel_type_label = 'Channel ' + row[COL_IN_OUT] + ' Lamelle'
        lamelle_channel_type = ohknx2.KnxRollershutterChannelType(row[COL_CHANNEL_NAME] + '_L', channel_type_label,
                                                                  row[COL_GA1], row[COL_GA2], row[COL_GA5],
                                                                  row[COL_GA6])
        device_thing.add_channel_type(lamelle_channel_type)

    def process_poweroutlet(self, row: dict):
        device_thing = self.get_knx_device_thing(row[COL_ACTUATOR_NAME], row[COL_ACTUATOR_LABEL],
                                                 row[COL_ACTUATOR_ADDRESS])
        channel_type_label = 'Channel ' + row[COL_IN_OUT]
        switch_channel_type = ohknx2.KnxSwitchChannelType(row[COL_CHANNEL_NAME], channel_type_label, row[COL_GA1],
                                                          row[COL_GA2])
        device_thing.add_channel_type(switch_channel_type)

    def write_config(self, filename: str):
        config_file = open(filename, 'w')

        config_file.write(self.bridge.get_config())

        config_file.close()


class ItemsConfigBuilder:
    def __init__(self, csv_reader: csv.DictReader):
        self.csv_reader = csv_reader
        self.items = []
        self.groups = {}
        self.lights_group = openhab2.Group(SWITCH_NAME_DYNAMIC_LIGHTS, SWITCH_NAME_DYNAMIC_LIGHTS, '[%d]',
                                           openhab2.ICON_LIGHT, 'Switch', 'OR(ON, OFF)')
        self.groups[self.lights_group.name] = self.lights_group

    def process_csv_input(self):
        for row in self.csv_reader:
            if row[COL_TYPE] == 'Lightbulb':
                self.process_lightbulb(row)
            elif row[COL_TYPE] == 'Dimmer':
                self.process_dimmer(row)
            elif row[COL_TYPE] == 'ContactSensor':
                self.process_contact_sensor(row)
            elif row[COL_TYPE] == 'Rollershutter':
                self.process_rollershutter(row)
            elif row[COL_TYPE] == 'Jalousie':
                self.process_jalousie(row)
            elif row[COL_TYPE] == 'PowerOutlet':
                self.process_poweroutlet(row)

    def write_config(self, filename: str):
        config_file = open(filename, 'w')

        config_file.write('// Groups\n')

        for key in self.groups.keys():
            config_file.write(self.groups[key].get_config() + '\n')

        config_file.write('\n// Items\n')

        for item in self.items:
            config_file.write(item.get_config() + '\n')

        config_file.close()

    def add_room_group(self, row: dict):
        room_name = row[COL_ROOM_NAME]
        if room_name not in self.groups:
            self.groups[room_name] = openhab2.Group(room_name, row[COL_ROOM_LABEL], '')

    def process_lightbulb(self, row: dict):
        self.add_room_group(row)
        lightbulb_item = ohknx2.SwitchItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_LIGHT, row[COL_ACTUATOR_NAME],
                                           row[COL_CHANNEL_NAME])
        lightbulb_item.add_group(self.lights_group.name)
        self.items.append(lightbulb_item)

    def process_dimmer(self, row: dict):
        self.add_room_group(row)
        dimmable_lightbulb_item = ohknx2.DimmableLightbuldItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_LIGHT,
                                                               row[COL_ACTUATOR_NAME], row[COL_CHANNEL_NAME])
        dimmable_lightbulb_item.add_group(self.lights_group.name)
        self.items.append(dimmable_lightbulb_item)

    def process_contact_sensor(self, row: dict):
        self.add_room_group(row)
        contact_sensor_item = ohknx2.ContactSensorItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_CONTACT,
                                                       row[COL_ACTUATOR_NAME], row[COL_CHANNEL_NAME])
        self.items.append(contact_sensor_item)

    def process_rollershutter(self, row: dict):
        self.add_room_group(row)
        rollershutter_item = ohknx2.RollershutterItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_CONTACT,
                                                      row[COL_ACTUATOR_NAME], row[COL_CHANNEL_NAME])
        self.items.append(rollershutter_item)

    def process_jalousie(self, row: dict):
        self.add_room_group(row)
        self.process_rollershutter(row)
        lamelle_item = ohknx2.RollershutterItem(row[COL_NAME] + '_Lamelle', row[COL_LABEL] + ' Lamelle',
                                                openhab2.ICON_CONTACT, row[COL_ACTUATOR_NAME],
                                                row[COL_CHANNEL_NAME] + '_L')
        self.items.append(lamelle_item)

    def process_poweroutlet(self, row: dict):
        self.add_room_group(row)
        power_outlet_item = ohknx2.SwitchItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_POWER_OUTLET,
                                        row[COL_ACTUATOR_NAME], row[COL_CHANNEL_NAME])
        power_outlet_item.add_group(self.lights_group.name)
        self.items.append(power_outlet_item)

    def add_special_items(self):
        disable_open_rollershutters = openhab2.Item('Switch', SWITCH_NAME_DISABLE_OPEN_BLINDS,
                                                    SWITCH_LABEL_DISABLE_OPEN_BLINDS, '[%s]', '')
        self.items.append(disable_open_rollershutters)


class SitemapConfigBuilder:
    def __init__(self, csv_reader: csv.DictReader):
        self.csv_reader = csv_reader
        self.frames = {}
        self.rooms = {}

        rooms_frame = openhab2.Frame('Räume')
        self.add_frame(FRAME_ALL_ROOMS, rooms_frame)
        dynamic_lights_frame = openhab2.Frame('Eingeschaltete Lampen')
        dynamic_lights_frame.add_sitemap_element(openhab2.SitemapSwitchElement(SWITCH_NAME_DYNAMIC_LIGHTS,
                                                                               SWITCH_LABEL_DYNAMIC_LIGHTS, '[%s]',
                                                                               openhab2.ICON_LIGHT))
        self.add_frame(FRAME_ACTIVE_LIGHTS, dynamic_lights_frame)
        dynamic_rollershutters_frame = openhab2.Frame('Offene Rolladen')
        self.add_frame(FRAME_OPEN_ROLLERSHUTTERS, dynamic_rollershutters_frame)
        special_functions_frame = openhab2.Frame('Spezialfunktionen')
        self.add_frame(FRAME_SPECIAL_FUNCTIONS, special_functions_frame)
        special_functions_frame.add_sitemap_element(openhab2.SitemapSwitchElement(SWITCH_NAME_DISABLE_OPEN_BLINDS,
                                                                                  SWITCH_LABEL_DISABLE_OPEN_BLINDS,
                                                                                  '[%s]', ''))

    def add_frame(self, frame_name: str, frame: openhab2.Frame):
        self.frames[frame_name] = frame

    def get_frame_by_name(self, frame_name: str) -> openhab2.Frame:
        return self.frames[frame_name]

    def process_csv_input(self):
        for row in self.csv_reader:
            if row[COL_TYPE] == 'Lightbulb':
                self.process_lightbulb(row)
            elif row[COL_TYPE] == 'Dimmer':
                self.process_dimmer(row)
            elif row[COL_TYPE] == 'ContactSensor':
                self.process_contact_sensor(row)
            elif row[COL_TYPE] == 'Rollershutter':
                self.process_rollershutter(row)
            elif row[COL_TYPE] == 'Jalousie':
                self.process_jalousie(row)
            elif row[COL_TYPE] == 'PowerOutlet':
                self.process_poweroutlet(row)

    def get_room_sitemap_element(self, room_name: str, room_label: str) -> openhab2.SitemapTextElement:
        if room_name in self.rooms:
            room_sitemap_element = self.rooms[room_name]
            return room_sitemap_element
        else:
            icon = SitemapConfigBuilder.get_room_icon(room_name)
            room_sitemap_element = openhab2.SitemapTextElement(room_name, room_label, '', icon)

            self.rooms[room_name] = room_sitemap_element
            frame = self.frames[FRAME_ALL_ROOMS]
            frame.add_sitemap_element(room_sitemap_element)
            return room_sitemap_element

    def process_lightbulb(self, row: dict):
        room_sitemap_element = self.get_room_sitemap_element(row[COL_ROOM_NAME], row[COL_ROOM_LABEL])
        switch_element = openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%s]', openhab2.ICON_LIGHT)
        room_sitemap_element.add_element(switch_element)
        self.get_frame_by_name(FRAME_ACTIVE_LIGHTS)\
            .add_sitemap_element(openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%s]',
                                                               openhab2.ICON_LIGHT, row[COL_NAME] + '==ON'))

    def process_dimmer(self, row: dict):
        room_sitemap_element = self.get_room_sitemap_element(row[COL_ROOM_NAME], row[COL_ROOM_LABEL])
        switch_element = openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%s]', openhab2.ICON_LIGHT)
        room_sitemap_element.add_element(switch_element)
        slider_element = openhab2.SitemapSliderElement(row[COL_NAME], row[COL_LABEL], '[%d %%]', openhab2.ICON_LIGHT)
        room_sitemap_element.add_element(slider_element)
        self.get_frame_by_name(FRAME_ACTIVE_LIGHTS)\
            .add_sitemap_element(openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%s]',
                                                               openhab2.ICON_LIGHT, row[COL_NAME] + '==ON'))

    def process_rollershutter(self, row: dict):
        room_sitemap_element = self.get_room_sitemap_element(row[COL_ROOM_NAME], row[COL_ROOM_LABEL])
        switch_element = openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%s]', openhab2.ICON_BLINDS)
        room_sitemap_element.add_element(switch_element)
        slider_element = openhab2.SitemapSliderElement(row[COL_NAME], row[COL_LABEL], '[%d %%]', openhab2.ICON_BLINDS)
        room_sitemap_element.add_element(slider_element)
        self.get_frame_by_name(FRAME_OPEN_ROLLERSHUTTERS)\
            .add_sitemap_element(openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%d %%]',
                                                               openhab2.ICON_BLINDS, row[COL_NAME] + '<100'))

    def process_jalousie(self, row: dict):
        room_sitemap_element = self.get_room_sitemap_element(row[COL_ROOM_NAME], row[COL_ROOM_LABEL])
        switch_element = openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%s]', openhab2.ICON_BLINDS)
        room_sitemap_element.add_element(switch_element)
        slider_element = openhab2.SitemapSliderElement(row[COL_NAME], row[COL_LABEL], '[%d %%]', openhab2.ICON_BLINDS)
        room_sitemap_element.add_element(slider_element)
        slider_element_lamelle = openhab2.SitemapSliderElement(row[COL_NAME] + '_Lamelle', row[COL_LABEL] + ' Lamelle',
                                                               '[%d %%]', openhab2.ICON_BLINDS)
        room_sitemap_element.add_element(slider_element_lamelle)
        self.get_frame_by_name(FRAME_OPEN_ROLLERSHUTTERS) \
            .add_sitemap_element(openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%d %%]',
                                                               openhab2.ICON_BLINDS, row[COL_NAME] + '<100'))

    def process_contact_sensor(self, row: dict):
        room_sitemap_element = self.get_room_sitemap_element(row[COL_ROOM_NAME], row[COL_ROOM_LABEL])
        text_element = openhab2.SitemapTextElement(row[COL_NAME], row[COL_LABEL], '', openhab2.ICON_CONTACT)
        room_sitemap_element.add_element(text_element)

    def process_poweroutlet(self, row: dict):
        room_sitemap_element = self.get_room_sitemap_element(row[COL_ROOM_NAME], row[COL_ROOM_LABEL])
        switch_element = openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%s]',
                                                       openhab2.ICON_POWER_OUTLET)
        room_sitemap_element.add_element(switch_element)
        self.get_frame_by_name(FRAME_ACTIVE_LIGHTS)\
            .add_sitemap_element(openhab2.SitemapSwitchElement(row[COL_NAME], row[COL_LABEL], '[%s]',
                                                               openhab2.ICON_POWER_OUTLET, row[COL_NAME] + '==ON'))

    def write_sitemap_config(self, filename: str, label: str):
        sitemap_config_file = open(filename, 'w')

        dot_idx = filename.find('.')
        sitemap_name = filename[:dot_idx]

        sitemap_config_file.write('sitemap ' + sitemap_name + ' label="' + label + '" {\n')

        sitemap_config_file.write(self.frames[FRAME_ALL_ROOMS].get_config())
        sitemap_config_file.write('\n')
        sitemap_config_file.write(self.frames[FRAME_ACTIVE_LIGHTS].get_config())
        sitemap_config_file.write('\n')
        sitemap_config_file.write(self.frames[FRAME_OPEN_ROLLERSHUTTERS].get_config())
        sitemap_config_file.write('\n')
        sitemap_config_file.write(self.frames[FRAME_SPECIAL_FUNCTIONS].get_config())
        sitemap_config_file.write('\n')

        sitemap_config_file.write('}')
        sitemap_config_file.close()

    @staticmethod
    def get_room_icon(room_name: str) -> str:
        if room_name.lower().find('garage') >= 0:
            return openhab2.ICON_GARAGE
        elif room_name.lower().find('kitchen') >= 0:
            return openhab2.ICON_KITCHEN
        elif room_name.lower().find('living_room') >= 0:
            return openhab2.ICON_LIVING_ROOM
        elif room_name.lower().find('bedroom') >= 0:
            return openhab2.ICON_BEDROOM
        elif room_name.lower().find('office') >= 0:
            return openhab2.ICON_OFFICE
        elif room_name.lower().find('bath') >= 0:
            return openhab2.ICON_BATH
        elif room_name.lower().find('boy') >= 0:
            return openhab2.ICON_BOY
        elif room_name.lower().find('girl') >= 0:
            return openhab2.ICON_GIRL
        elif room_name.lower().find('corridor') >= 0:
            return openhab2.ICON_CORRIDOR
        elif room_name.lower().find('toilet') >= 0:
            return openhab2.ICON_TOILET
        elif room_name.lower().find('utility_room') >= 0:
            return openhab2.ICON_WASHINGMACHINE
        else:
            return openhab2.ICON_GROUP


csv_knx_file = open('../docs/oh2_knx2.csv', 'rt')
knx_fieldnames = [COL_ACTUATOR_NAME, COL_ACTUATOR_LABEL, COL_ACTUATOR_ADDRESS, COL_CHANNEL_NAME, COL_IN_OUT, COL_TYPE,
                  COL_GA1, COL_GA2, COL_GA3, COL_GA4, COL_GA5, COL_GA6]
csv_knx_reader = csv.DictReader(csv_knx_file, knx_fieldnames)

knx_things_config_builder = KnxThingsConfigBuilder(csv_knx_reader)
knx_things_config_builder.process_csv_input()
knx_things_config_builder.write_config('knx.things')

csv_items_file = open('../docs/oh2_items.csv')
items_fieldnames = [COL_NAME, COL_LABEL, COL_FLOOR, COL_ROOM_NAME, COL_ROOM_LABEL, COL_TYPE, COL_ACTUATOR_NAME,
                    COL_CHANNEL_NAME]
csv_items_reader = csv.DictReader(csv_items_file, items_fieldnames)

items_config_builder = ItemsConfigBuilder(csv_items_reader)
items_config_builder.process_csv_input()
items_config_builder.add_special_items()
items_config_builder.write_config('knx2.items')

csv_items_file.seek(0)

sitemap_config_builder = SitemapConfigBuilder(csv_items_reader)
sitemap_config_builder.process_csv_input()
sitemap_config_builder.write_sitemap_config('our_home.sitemap', 'Haus')
