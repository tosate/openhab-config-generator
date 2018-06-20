import openhab2
import ohknx2
import homekit


knx_device = ohknx2.KnxThing('generic', '1.1.1')
lamp = ohknx2.SwitchItem('my_lamp', 'Living Room Lamp', openhab2.ICON_LIGHT, '3/0/4', '3/0/5')
lamp.add_tag(homekit.LIGHTING)
knx_device.add_item(lamp)
contact = ohknx2.ContactItem('my_contact_sensor', 'Window Contact', '1/2/3')
knx_device.add_item(contact)
dimmer = ohknx2.DimmerItem('my_dimmer', 'Living Room Dimmer', openhab2.ICON_LIGHT, '1/0/1', '1/1/1', '1/2/1', '1/3/1',
                           '1/4/1')
dimmer.add_tag(homekit.LIGHTING)
knx_device.add_item(dimmer)
rollershutter = ohknx2.RollershutterItem('my_rollershutter', 'Rollershutter Living Room', '2/0/1', '2/1/1', '2/2/1',
                                         '2/3/1')
rollershutter.add_tag(homekit.BLINDS)
knx_device.add_item(rollershutter)
knx_bridge = ohknx2.KnxBridge('192.168.0.10', 3671, '192.168.0.11')
knx_bridge.add_thing(knx_device)
#print(knx_bridge.get_config())

print(lamp.get_config())
print(contact.get_config())
print(dimmer.get_config())
print(rollershutter.get_config())