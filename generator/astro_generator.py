import openhab2

LATITUDE = '49.60112'
LONGITUDE = '6.56834'
ALTITUDE = '200'
INTERVAL = 300

ASTRO_BINDING_ID = 'astro'
SUN_TYPE_ID = 'sun'
MOON_TYPE_ID = 'moon'

RANGE_EVENT_CHANNEL = 'rangeEvent'

RISE_GROUP = 'rise'
SET_GROUP = 'set'

START_EVENT = 'start'


class AstroTriggerChannelType:
    def __init__(self, channel_type: str, group: str, earliest: str=None, latest: str=None):
        self.channel_type = channel_type
        self.group = group
        self.event = 'event'
        if earliest:
            self.parameters = {'earliest': earliest}
        if latest:
            self.parameters = {'latest': latest}
        self.tab_level = 2

    def get_channel_config(self) -> str:
        config = 'Type ' + self.channel_type + ' : ' + self.group + '#' + self.event + ' ['

        for key in self.parameters.keys():
            if type(self.parameters.get(key)) is str:
                config = config + '\n' + '\t' * (self.tab_level+1) + '{}="{}",'.format(key, self.parameters.get(key))
            elif type(self.parameters.get(key)) is int:
                config = config + '\n' + '\t' * (self.tab_level+1) + '{}={},'.format(key, self.parameters.get(key))

        config = config[:len(config)-1] + '\n' + '\t' * (self.tab_level-1) + ']'

        return config


class AstroThing(openhab2.Thing):
    def __init__(self, type_id: str, thing_id: str, label: str):
        openhab2.Thing.__init__(self, ASTRO_BINDING_ID, type_id, thing_id, label, '')

        self.parameters['geolocation'] = LATITUDE + ',' + LONGITUDE + ',' + ALTITUDE
        self.parameters['interval'] = INTERVAL

    def add_channel_type(self, channel_type: AstroTriggerChannelType):
        self.items.append(channel_type)

    def get_astro_config(self):
        config = self.get_config()

        if len(self.items) > 0:
            config = config + ' {' + '\n' + '\t' * self.tab_level + ' Channels: '

            for item in self.items:
                config = config + '\n' + '\t' * (self.tab_level+1) + item.get_channel_config()
            config = config + '\n' + '\t' * (self.tab_level-1) + '}'

        config = config + '\n\n'

        return config


class AstroThingsConfigBuilder:
    def __init__(self):
        self.astro_things = []

    def generate_things(self):
        astro_thing_sun_home = AstroThing(SUN_TYPE_ID, 'sun', 'Sonne')
        self.astro_things.append(astro_thing_sun_home)

        astro_thing_moon_home = AstroThing(MOON_TYPE_ID, 'moon', 'Mond')
        self.astro_things.append(astro_thing_moon_home)

        trigger_sunset_latest1830 = AstroTriggerChannelType(RANGE_EVENT_CHANNEL, SET_GROUP, None, '18:30')
        astro_thing_sunset_latest1830 = AstroThing(SUN_TYPE_ID, 'closeShuttersKids', 'Rolladen Kinderzimmer schliessen')
        astro_thing_sunset_latest1830.add_channel_type(trigger_sunset_latest1830)
        self.astro_things.append(astro_thing_sunset_latest1830)

        trigger_sunset_latest2200 = AstroTriggerChannelType(RANGE_EVENT_CHANNEL, SET_GROUP, None, '22:20')
        astro_thing_sunset_latest2220 = AstroThing(SUN_TYPE_ID, 'closeShutters', 'Rolladen schliessen')
        astro_thing_sunset_latest2220.add_channel_type(trigger_sunset_latest2200)
        self.astro_things.append(astro_thing_sunset_latest2220)

        trigger_sunset_earliest2000 = AstroTriggerChannelType(RANGE_EVENT_CHANNEL, SET_GROUP, '20:00')
        astro_thing_tv_night = AstroThing(SUN_TYPE_ID, 'eveningLights', 'Abendbeleuchtung einschalten')
        astro_thing_tv_night.add_channel_type(trigger_sunset_earliest2000)
        self.astro_things.append(astro_thing_tv_night)

        trigger_sunrise_earliest0700 = AstroTriggerChannelType(RANGE_EVENT_CHANNEL, RISE_GROUP, '07:00')
        astro_thing_sunrise_earliest0700 = AstroThing(SUN_TYPE_ID, 'openShuttersDaily', 'Rolladen öffnen werktags')
        astro_thing_sunrise_earliest0700.add_channel_type(trigger_sunrise_earliest0700)
        self.astro_things.append(astro_thing_sunrise_earliest0700)

        trigger_sunrise_earliest0730 = AstroTriggerChannelType(RANGE_EVENT_CHANNEL, RISE_GROUP, '07:30')
        astro_thing_sunrise_earliest0730 = AstroThing(SUN_TYPE_ID, 'openShuttersWe', 'Rolladen öffnen Wochenende')
        astro_thing_sunrise_earliest0730.add_channel_type(trigger_sunrise_earliest0730)
        self.astro_things.append(astro_thing_sunrise_earliest0730)

    def write_config(self, filename: str):
        self.generate_things()

        config_file = open(filename, 'w')

        for astro_thing in self.astro_things:
            config_file.write(astro_thing.get_astro_config())

        config_file.close()


astro_things_config_builder = AstroThingsConfigBuilder()
astro_things_config_builder.write_config('astro.things')