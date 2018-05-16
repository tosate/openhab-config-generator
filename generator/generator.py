import csv
from doctest import _ellipsis_match

import ohobjects

COLUMN_NAME = 'name'
COLUMN_LABEL = 'label'
COLUMN_FLOOR = 'floor'
COLUMN_ROOM_NAME = 'room_name'
COLUMN_ROOM_LABEL = 'room_label'
COLUMN_TYPE = 'type'
COLUMN_GA1 = 'ga1'
COLUMN_GA2 = 'ga2'
COLUMN_GA3 = 'ga3'
COLUMN_GA4 = 'ga4'
COLUMN_GA5 = 'ga5'
COLUMN_GA6 = 'ga6'


class ItemConfig:
    def __init__(self, main_group: ohobjects.Group):
        self.main_group = main_group
        self.location_groups = []
        self.function_groups = []
        self.items = []

    def add_location_group(self, group: ohobjects.Group):
        self.location_groups.append(group)

    def add_function_group(self, group: ohobjects.Group):
        self.function_groups.append(group)

    def add_item(self, item: ohobjects.Item):
        self.items.append(item)

    def write_item_config(self, filename: str):
        item_config_file = open(filename, 'w')

        item_config_file.write(self.main_group.get_config() + '\n')

        item_config_file.write('\n// Locations\n')

        for location_group in self.location_groups:
            item_config_file.write(location_group.get_config() + '\n')

        item_config_file.write('\n// Functions\n')

        for function_group in self.function_groups:
            item_config_file.write(function_group.get_config() + '\n')

        item_config_file.write('\n// Items\n')

        for item in self.items:
            item_config_file.write(item.get_config() + '\n')

        item_config_file.close()


class SitemapConfig:
    def __init__(self):
        self.frames = {}

    def add_frame(self, frame: ohobjects.Frame):
        self.frames[frame.label] = frame

    def get_frame_by_label(self, label: str) -> ohobjects.Frame:
        return self.frames[label]

    def write_sitemap_config(self, filename: str, label: str):
        sitemap_config_file = open(filename, 'w')

        dot_idx = filename.find('.')
        sitemap_name = filename[:dot_idx]

        sitemap_config_file.write('sitemap ' + sitemap_name + ' label="' + label + '" {\n')

        for key in self.frames:
            sitemap_config_file.write(self.frames[key].get_config())
            sitemap_config_file.write('\n')

        sitemap_config_file.write('}')
        sitemap_config_file.close()


class ConfigBuilder:
    def __init__(self, csv_reader: csv.DictReader):
        self.csv_reader = csv_reader

        # Prepare groups
        self.house_group = ohobjects.Group('House', 'Haus', ohobjects.ICON_HOUSE)
        self.ground_floor_group = ohobjects.Group('GroundFloor', 'Erdgeschoss', ohobjects.ICON_GROUNDFLOOR)
        self.ground_floor_group.add_group(self.house_group)
        self.first_floor_group = ohobjects.Group('FirstFloor', 'Obergeschoss', ohobjects.ICON_FIRSTFLOOR)
        self.first_floor_group.add_group(self.house_group)
        self.lights_group = ohobjects.Group('Lights', 'Lichter', ohobjects.ICON_LIGHT)
        self.lights_group.add_group(self.house_group)
        self.rollershutters_group = ohobjects.Group('Rollershutters', 'Rolladen', ohobjects.ICON_BLINDS)
        self.rollershutters_group.add_group(self.house_group)
        self.contact_sensors_group = ohobjects.Group('ContactSensors', 'Kontaktsensoren', ohobjects.ICON_CONTACT)
        self.contact_sensors_group.add_group(self.house_group)

        # Prepare frames
        self.rooms_frame = ohobjects.Frame('Räume')

        self.item_configuration = ItemConfig(self.house_group)
        self.item_configuration.add_location_group(self.ground_floor_group)
        self.item_configuration.add_location_group(self.first_floor_group)
        self.item_configuration.add_function_group(self.lights_group)
        self.item_configuration.add_function_group(self.contact_sensors_group)
        self.item_configuration.add_function_group(self.rollershutters_group)

        self.sitemap_config = SitemapConfig()
        self.sitemap_config.add_frame(self.rooms_frame)

        self.rooms = {}

    def process_csv_input(self):
        for row in self.csv_reader:
            if row[COLUMN_TYPE] == 'Lightbulb':
                self.process_lightbulb(row)
            elif row[COLUMN_TYPE] == 'ContactSensor':
                self.process_contact_sensor(row)
            elif row[COLUMN_TYPE] == 'Rollershutter':
                self.process_rollershutter(row)
            elif row[COLUMN_TYPE] == 'Jalousie':
                self.process_jalousie(row)
            else:
                print(row[COLUMN_LABEL], row[COLUMN_GA1])

    def get_item_config(self) -> ItemConfig:
        return self.item_configuration

    def get_sitemap_config(self) -> SitemapConfig:
        return self.sitemap_config

    def process_floor_and_room(self, item: ohobjects.Item, floor: str, room_name: str, room_label: str):
        if floor == 'GF':
            item.add_group(self.ground_floor_group)
        elif floor == 'FF':
            item.add_group(self.first_floor_group)

        if room_name in self.rooms:
            room_sitemap_element = self.rooms[room_name]
            item.add_group(room_sitemap_element.item)
            for element in item.get_sitemap_elements():
                room_sitemap_element.add_element(element)
        else:
            icon = ConfigBuilder.get_room_icon(room_name)
            room_group = ohobjects.Group(room_name, room_label, icon)
            item.add_group(room_group)
            room_sitemap_element = ohobjects.SitemapTextElement(room_group)
            for element in item.get_sitemap_elements():
                room_sitemap_element.add_element(element)

            self.rooms[room_name] = room_sitemap_element
            self.item_configuration.add_location_group(room_group)
            frame = self.sitemap_config.get_frame_by_label('Räume')
            frame.add_sitemap_element(room_sitemap_element)

    @staticmethod
    def get_room_icon(room_name: str) -> str:
        if room_name.lower().find('garage') >= 0:
            return ohobjects.ICON_GARAGE
        elif room_name.lower().find('kitchen') >= 0:
            return ohobjects.ICON_KITCHEN
        elif room_name.lower().find('living_room') >= 0:
            return ohobjects.ICON_LIVING_ROOM
        elif room_name.lower().find('bedroom') >= 0:
            return ohobjects.ICON_BEDROOM
        elif room_name.lower().find('office') >= 0:
            return ohobjects.ICON_OFFICE
        elif room_name.lower().find('bath') >= 0:
            return ohobjects.ICON_BATH
        elif room_name.lower().find('boy') >= 0:
            return ohobjects.ICON_BOY
        elif room_name.lower().find('girl') >= 0:
            return ohobjects.ICON_GIRL
        elif room_name.lower().find('corridor') >= 0:
            return ohobjects.ICON_CORRIDOR
        elif room_name.lower().find('toilet') >= 0:
            return ohobjects.ICON_TOILET
        elif room_name.lower().find('utility_room') >= 0:
            return ohobjects.ICON_WASHINGMACHINE
        else:
            return ohobjects.ICON_GROUP

    def process_lightbulb(self, row: dict):
        lightbulb = ohobjects.LightbulbItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_LIGHT,
                                            row[COLUMN_GA1], row[COLUMN_GA2])
        lightbulb.add_group(self.house_group)
        lightbulb.add_group(self.lights_group)
        self.process_floor_and_room(lightbulb, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME], row[COLUMN_ROOM_LABEL])
        self.item_configuration.add_item(lightbulb)

    def process_contact_sensor(self, row: dict):
        contact_sensor = ohobjects.ContactSensorItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_CONTACT,
                                                     row[COLUMN_GA1])
        contact_sensor.add_group(self.house_group)
        contact_sensor.add_group(self.contact_sensors_group)
        self.process_floor_and_room(contact_sensor, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME],
                                    row[COLUMN_ROOM_LABEL])
        self.item_configuration.add_item(contact_sensor)

    def process_rollershutter(self, row: dict):
        rollershutter = ohobjects.RollershutterItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_BLINDS,
                                                    row[COLUMN_GA1], row[COLUMN_GA2], row[COLUMN_GA3], row[COLUMN_GA4])
        rollershutter.add_group(self.house_group)
        rollershutter.add_group(self.rollershutters_group)
        self.process_floor_and_room(rollershutter, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME], row[COLUMN_ROOM_LABEL])
        self.item_configuration.add_item(rollershutter)

    def process_jalousie(self, row: dict):
        jalousie = ohobjects.JalousieItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_BLINDS, row[COLUMN_GA1],
                                          row[COLUMN_GA2], row[COLUMN_GA3], row[COLUMN_GA4], row[COLUMN_GA5],
                                          row[COLUMN_GA6])
        jalousie.add_group(self.house_group)
        jalousie.add_group(self.rollershutters_group)
        self.process_floor_and_room(jalousie, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME], row[COLUMN_ROOM_LABEL])
        self.item_configuration.add_item(jalousie)


csv_file = open('../docs/openhab2.csv', 'rt')
fieldnames = [COLUMN_NAME, COLUMN_LABEL, COLUMN_FLOOR, COLUMN_ROOM_NAME, COLUMN_ROOM_LABEL, COLUMN_TYPE, COLUMN_GA1,
              COLUMN_GA2, COLUMN_GA3, COLUMN_GA4, COLUMN_GA5, COLUMN_GA6]
csv_reader = csv.DictReader(csv_file, fieldnames)

config_builder = ConfigBuilder(csv_reader)
config_builder.process_csv_input()

item_config = config_builder.get_item_config()
item_config.write_item_config('knx.items')

sitemap_config = config_builder.get_sitemap_config()
sitemap_config.write_sitemap_config('our_home.sitemap', 'Haus')

