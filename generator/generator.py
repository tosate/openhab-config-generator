import csv

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

FRAME_ALL_ROOMS = 'ALL_ROOMS'
FRAME_ACTIVE_LIGHTS = 'ACTIVE_LIGHTS'
FRAME_OPEN_ROLLERSHUTTERS = 'OPEN_ROLLERSHUTTERS'
FRAME_SPECIAL_FUNCTIONS = 'SPECIAL_FUNCTIONS'


class ItemConfig:
    def __init__(self, main_group: ohobjects.Group):
        self.main_group = main_group
        self.items = []

    def add_item(self, item: ohobjects.Item):
        self.items.append(item)


class AstroItemConfig(ItemConfig):
    def __init__(self, main_group: ohobjects.Group):
        ItemConfig.__init__(self, main_group)
        self.items = list(self.get_astro_items().values())

    def get_astro_items(self) -> dict:
        result = {}
        # group
        astro_group = ohobjects.Group('Astro', 'Astro', ohobjects.ICON_SUN_CLOUDS)
        result[astro_group.name] = astro_group
        # items
        today = ohobjects.DateTimeItem('Current_Date_Time', 'Today', '[%1$tA, %1$td.%1$tm.%1$tY]', ohobjects.ICON_CLOCK,
                                       'ntp:ntp:local:dateTime')
        today.add_group(astro_group)
        result[today.name] = today
        sunset = ohobjects.DateTimeItem('Sunset_Time', 'Sunset', '[%1$tH:%1$tM]', ohobjects.ICON_SUN,
                                        'astro:sun:home:set#start')
        sunset.add_group(astro_group)
        result[sunset.name] = sunset
        sunrise = ohobjects.DateTimeItem('Sunrise_Time', 'Sunrise', '[%1$tH:%1$tM]', ohobjects.ICON_SUN,
                                         'astro:sun:home:rise#end')
        sunrise.add_group(astro_group)
        result[sunrise.name] = sunrise
        evening = ohobjects.DateTimeItem('Evening_Time', 'Evening', '[%1$tH:%1$tM]', '', 'astro:sun:minus90:set#start')
        evening.add_group(astro_group)
        result[evening.name] = evening
        day_phase = ohobjects.StringItem('Day_Phase', 'Phase of Day', '[Map(astro.map):%s]', '',
                                         'astro:sun:home:phase#name')
        day_phase.add_group(astro_group)
        result[day_phase.name] = day_phase
        night_state_switch = ohobjects.SwitchItem('Night_State', 'Night')
        night_state_switch.add_group(astro_group)
        result[night_state_switch.name] = night_state_switch
        season_name = ohobjects.StringItem('Season_Name', 'Season', '[Map(astro.map):%s]', '',
                                           'astro:sun:home:season#name')
        season_name.add_group(astro_group)
        result[season_name.name] = season_name
        sun_elevation = ohobjects.NumberItem('Sun_Elevation', 'Sun Elevation', '[%.1f °]', ohobjects.ICON_SUN,
                                             'astro:sun:home:position#elevation')
        sun_elevation.add_group(astro_group)
        result[sun_elevation.name] = sun_elevation
        moon_elevation = ohobjects.NumberItem('Moon_Elevation', 'Moon Elevation', '[%.1f °]', ohobjects.ICON_MOON,
                                              'astro:moon:home:position#elevation')
        moon_elevation.add_group(astro_group)
        result[moon_elevation.name] = moon_elevation
        moon_phase = ohobjects.StringItem('Moon_Phase', 'Moon Phase', '[Map(astro.map):%s]', ohobjects.ICON_MOON,
                                          'astro:moon:home:phase#name')
        moon_phase.add_group(astro_group)
        result[moon_phase.name] = moon_phase
        moon_next_full = ohobjects.DateTimeItem('Moon_Next_Full', 'Next Full Moon', '[%1$td.%1$tm.%1$tY, %1$tH:%1$tM]',
                                                ohobjects.ICON_MOON, 'astro:moon:home:phase#full')
        moon_next_full.add_group(astro_group)
        result[moon_next_full.name] = moon_next_full
        moon_next_new = ohobjects.DateTimeItem('Moon_Next_New', 'Next New Moon', '[%1$td.%1$tm.%1$tY, %1$tH:%1$tM]',
                                               ohobjects.ICON_MOON, 'astro:moon:home:phase#new')
        moon_next_new.add_group(astro_group)
        result[moon_next_new.name] = moon_next_new
        return result

    def write_item_config(self, filename: str):
        item_config_file = open(filename, 'w')

        for item in self.items:
            item_config_file.write(item.get_config() + '\n')

        item_config_file.close()


class KnxItemConfig(ItemConfig):
    def __init__(self, main_group: ohobjects.Group):
        ItemConfig.__init__(self, main_group)
        self.location_groups = []
        self.function_groups = []

    def add_location_group(self, group: ohobjects.Group):
        self.location_groups.append(group)

    def add_function_group(self, group: ohobjects.Group):
        self.function_groups.append(group)

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

        item_config_file.write('\n// Special items\n')

        for item in self.get_special_items():
            item_config_file.write(item.get_config() + '\n')

        item_config_file.close()

    def get_special_items(self) -> list:
        result = []
        disable_open_rollershutters = ohobjects.SwitchItem("Disable_Open_Rollershutters", "Rolläden nicht öffnen", '[%s]')
        result.append(disable_open_rollershutters)
        return result


class SitemapConfig:
    def __init__(self):
        self.frames = {}

    def add_frame(self, frame_name: str, frame: ohobjects.Frame):
        self.frames[frame_name] = frame

    def get_frame_by_name(self, frame_name: str) -> ohobjects.Frame:
        return self.frames[frame_name]


class KnxSitemapConfig(SitemapConfig):
    def __init__(self):
        SitemapConfig.__init__(self)

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


class AstroSitemapConfig(SitemapConfig):
    def __init__(self):
        SitemapConfig.__init__(self)

    def get_astro_sitemap_element(self, astro_items: dict) -> ohobjects.SitemapTextElement:
        main_text_element = ohobjects.SitemapTextElement(astro_items['Current_Date_Time'])
        frame = ohobjects.Frame('Now')
        main_text_element.add_element(frame)
        day_phase_element = ohobjects.SitemapTextElement(astro_items['Day_Phase'])
        frame.add_sitemap_element(day_phase_element)
        return main_text_element

    def write_sitemap_config(self, filename: str, label: str):
        sitemap_config_file = open(filename, 'w')

        dot_idx = filename.find('.')
        sitemap_name = filename[:dot_idx]

        sitemap_config_file.write('sitemap ' + sitemap_name + ' label="' + label + '" {\n')
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
        self.switch_off_active_lights_group = ohobjects.Group('Lights', 'Eingeschaltete Lampen [%d]', ohobjects.ICON_LIGHT, 'Switch', 'OR(ON, OFF)')
        self.switch_off_active_lights_group.add_group(self.house_group)
        self.rollershutters_group = ohobjects.Group('Rollershutters', 'Rolladen', ohobjects.ICON_BLINDS)
        self.rollershutters_group.add_group(self.house_group)
        self.contact_sensors_group = ohobjects.Group('ContactSensors', 'Kontaktsensoren', ohobjects.ICON_CONTACT)
        self.contact_sensors_group.add_group(self.house_group)

        # Prepare frames
        self.rooms_frame = ohobjects.Frame('Räume')
        self.dynamic_lights_frame = ohobjects.Frame('Eingeschaltete Lampen')
        self.dynamic_dimmers_frame = ohobjects.Frame('Eingeschaltete Dimmer')
        self.dynamic_rollershutters_frame = ohobjects.Frame('Offene Rolladen')
        self.special_functions_frame = ohobjects.Frame('Spezialfunktionen')

        self.knx_item_configuration = KnxItemConfig(self.house_group)
        self.knx_item_configuration.add_location_group(self.ground_floor_group)
        self.knx_item_configuration.add_location_group(self.first_floor_group)
        self.knx_item_configuration.add_function_group(self.switch_off_active_lights_group)
        self.knx_item_configuration.add_function_group(self.contact_sensors_group)
        self.knx_item_configuration.add_function_group(self.rollershutters_group)

        self.astro_item_configuration = AstroItemConfig(None)

        self.sitemap_config = KnxSitemapConfig()
        self.sitemap_config.add_frame(FRAME_ALL_ROOMS, self.rooms_frame)
        self.sitemap_config.add_frame(FRAME_ACTIVE_LIGHTS, self.dynamic_lights_frame)
        self.sitemap_config.add_frame(FRAME_OPEN_ROLLERSHUTTERS, self.dynamic_rollershutters_frame)
        self.sitemap_config.add_frame(FRAME_SPECIAL_FUNCTIONS, self.special_functions_frame)

        switch_off_active_lights_site_element = ohobjects.SitemapSwitchElement(self.switch_off_active_lights_group)
        self.sitemap_config.get_frame_by_name(FRAME_ACTIVE_LIGHTS).add_sitemap_element(switch_off_active_lights_site_element)

        self.rooms = {}

    def process_csv_input(self):
        for row in self.csv_reader:
            if row[COLUMN_TYPE] == 'Lightbulb':
                self.process_lightbulb(row)
            elif row[COLUMN_TYPE] == 'Dimmer':
                self.process_dimmer(row)
            elif row[COLUMN_TYPE] == 'ContactSensor':
                self.process_contact_sensor(row)
            elif row[COLUMN_TYPE] == 'Rollershutter':
                self.process_rollershutter(row)
            elif row[COLUMN_TYPE] == 'Jalousie':
                self.process_jalousie(row)
            else:
                print(row[COLUMN_LABEL], row[COLUMN_GA1])

    def get_knx_item_config(self) -> KnxItemConfig:
        return self.knx_item_configuration

    def get_astro_item_config(self) -> AstroItemConfig:
        return self.astro_item_configuration

    def get_knx_sitemap_config(self) -> KnxSitemapConfig:
        self.init_special_functions_frame()
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
            if floor == 'GF':
                room_group.add_group(self.ground_floor_group)
            elif floor == 'FF':
                room_group.add_group(self.first_floor_group)
            item.add_group(room_group)
            room_sitemap_element = ohobjects.SitemapTextElement(room_group)
            for element in item.get_sitemap_elements():
                room_sitemap_element.add_element(element)

            self.rooms[room_name] = room_sitemap_element
            self.knx_item_configuration.add_location_group(room_group)
            frame = self.sitemap_config.get_frame_by_name(FRAME_ALL_ROOMS)
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

    def init_special_functions_frame(self):
        for item in self.knx_item_configuration.get_special_items():
            frame = self.sitemap_config.frames[FRAME_SPECIAL_FUNCTIONS]
            frame.add_sitemap_element(item.get_sitemap_element())

    def process_lightbulb(self, row: dict):
        lightbulb = ohobjects.LightbulbItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_LIGHT,
                                            row[COLUMN_GA1], row[COLUMN_GA2])
        lightbulb.add_group(self.house_group)
        lightbulb.add_group(self.switch_off_active_lights_group)
        self.process_floor_and_room(lightbulb, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME], row[COLUMN_ROOM_LABEL])
        self.knx_item_configuration.add_item(lightbulb)
        self.dynamic_lights_frame.add_sitemap_element(lightbulb.get_dynamic_sitemap_element())

    def process_dimmer(self, row: dict):
        self.process_lightbulb(row)

        dimmer = ohobjects.DimmableLightbuldItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_LIGHT,
                                                 row[COLUMN_GA1], row[COLUMN_GA2], row[COLUMN_GA3], row[COLUMN_GA4],
                                                 row[COLUMN_GA5])
        dimmer.add_group(self.house_group)
        dimmer.add_group(self.switch_off_active_lights_group)
        self.process_floor_and_room(dimmer, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME], row[COLUMN_ROOM_LABEL])
        self.knx_item_configuration.add_item(dimmer)

    def process_contact_sensor(self, row: dict):
        contact_sensor = ohobjects.ContactSensorItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_CONTACT,
                                                     row[COLUMN_GA1])
        contact_sensor.add_group(self.house_group)
        contact_sensor.add_group(self.contact_sensors_group)
        self.process_floor_and_room(contact_sensor, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME],
                                    row[COLUMN_ROOM_LABEL])
        self.knx_item_configuration.add_item(contact_sensor)

    def process_rollershutter(self, row: dict):
        rollershutter = ohobjects.RollershutterItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_BLINDS,
                                                    row[COLUMN_GA1], row[COLUMN_GA2], row[COLUMN_GA3], row[COLUMN_GA4])
        rollershutter.add_group(self.house_group)
        rollershutter.add_group(self.rollershutters_group)
        self.process_floor_and_room(rollershutter, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME], row[COLUMN_ROOM_LABEL])
        self.knx_item_configuration.add_item(rollershutter)
        self.dynamic_rollershutters_frame.add_sitemap_element(rollershutter.get_dynamic_sitemap_element())

    def process_jalousie(self, row: dict):
        jalousie = ohobjects.JalousieItem(row[COLUMN_NAME], row[COLUMN_LABEL], ohobjects.ICON_BLINDS, row[COLUMN_GA1],
                                          row[COLUMN_GA2], row[COLUMN_GA3], row[COLUMN_GA4], row[COLUMN_GA5],
                                          row[COLUMN_GA6])
        jalousie.add_group(self.house_group)
        jalousie.add_group(self.rollershutters_group)
        self.process_floor_and_room(jalousie, row[COLUMN_FLOOR], row[COLUMN_ROOM_NAME], row[COLUMN_ROOM_LABEL])
        self.knx_item_configuration.add_item(jalousie)
        self.dynamic_rollershutters_frame.add_sitemap_element(jalousie.get_dynamic_sitemap_element())


csv_file = open('../docs/openhab2.csv', 'rt')
fieldnames = [COLUMN_NAME, COLUMN_LABEL, COLUMN_FLOOR, COLUMN_ROOM_NAME, COLUMN_ROOM_LABEL, COLUMN_TYPE, COLUMN_GA1,
              COLUMN_GA2, COLUMN_GA3, COLUMN_GA4, COLUMN_GA5, COLUMN_GA6]
csv_reader = csv.DictReader(csv_file, fieldnames)

config_builder = ConfigBuilder(csv_reader)
config_builder.process_csv_input()

knx_item_config = config_builder.get_knx_item_config()
knx_item_config.write_item_config('knx.items')

sitemap_config = config_builder.get_knx_sitemap_config()
sitemap_config.write_sitemap_config('our_home.sitemap', 'Haus')

astro_item_config = config_builder.get_astro_item_config()
astro_item_config.write_item_config('astro.items')

