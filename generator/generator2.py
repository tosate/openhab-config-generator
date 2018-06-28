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

    def write_config(self, filename: str):
        config_file = open(filename, 'w')

        config_file.write(self.bridge.get_config())

        config_file.close()


class ItemsConfigBuilder:
    def __init__(self, csv_reader: csv.DictReader):
        self.csv_reader = csv_reader
        self.items = []

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

    def write_config(self, filename: str):
        config_file = open(filename, 'w')

        for item in self.items:
            config_file.write(item.get_config() + '\n')

        config_file.close()

    def process_lightbulb(self, row: dict):
        lightbulb_item = ohknx2.SwitchItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_LIGHT, row[COL_ACTUATOR_NAME],
                                           row[COL_CHANNEL_NAME])
        self.items.append(lightbulb_item)

    def process_dimmer(self, row: dict):
        dimmable_lightbulb_item = ohknx2.DimmableLightbuldItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_LIGHT,
                                                   row[COL_ACTUATOR_NAME], row[COL_CHANNEL_NAME])
        self.items.append(dimmable_lightbulb_item)

    def process_contact_sensor(self, row: dict):
        contact_sensor_item = ohknx2.ContactSensorItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_CONTACT,
                                                   row[COL_ACTUATOR_NAME], row[COL_CHANNEL_NAME])
        self.items.append(contact_sensor_item)

    def process_rollershutter(self, row: dict):
        rollershutter_item = ohknx2.RollershutterItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_CONTACT,
                                                   row[COL_ACTUATOR_NAME], row[COL_CHANNEL_NAME])
        self.items.append(rollershutter_item)

    def process_jalousie(self, row: dict):
        jalousie_item = ohknx2.RollershutterItem(row[COL_NAME], row[COL_LABEL], openhab2.ICON_CONTACT,
                                                   row[COL_ACTUATOR_NAME], row[COL_CHANNEL_NAME])
        self.items.append(jalousie_item)


csv_knx_file = open('../docs/oh2_knx2.csv', 'rt')
knx_fieldnames = [COL_ACTUATOR_NAME, COL_ACTUATOR_LABEL, COL_ACTUATOR_ADDRESS, COL_CHANNEL_NAME, COL_IN_OUT, COL_TYPE,
                  COL_GA1, COL_GA2, COL_GA3, COL_GA4, COL_GA5, COL_GA6]
csv_knx_reader = csv.DictReader(csv_knx_file, knx_fieldnames)

knx_thimgs_config_builder = KnxThingsConfigBuilder(csv_knx_reader)
knx_thimgs_config_builder.process_csv_input()
knx_thimgs_config_builder.write_config('knx.things')

csv_items_file = open('../docs/oh2_items.csv')
items_fieldnames = [COL_NAME, COL_LABEL, COL_FLOOR, COL_ROOM_NAME, COL_ROOM_LABEL, COL_TYPE, COL_ACTUATOR_NAME,
                    COL_CHANNEL_NAME]
csv_items_reader = csv.DictReader(csv_items_file, items_fieldnames)

items_config_builder = ItemsConfigBuilder(csv_items_reader)
items_config_builder.process_csv_input()
items_config_builder.write_config('knx2.items')
