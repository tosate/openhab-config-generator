import openhab2
import ohknx2


knx_device = ohknx2.KnxThing('generic', '1.1.1')
lamp = ohknx2.SwitchItem('my_lamp', 'Living Room Lamp', openhab2.ICON_LIGHT, '3/0/4', '3/0/5')
knx_device.add_item(lamp)
contact = ohknx2.ContactItem('my_contact_sensor', 'Window Contact', '1/2/3')
knx_device.add_item(contact)
dimmer = ohknx2.DimmerItem('my_dimmer', 'Living Room Dimmer', openhab2.ICON_LIGHT, '1/0/1', '1/1/1', '1/2/1', '1/3/1',
                           '1/4/1')
knx_device.add_item(dimmer)
rollershutter = ohknx2.RollershutterItem('my_rollershutter', 'Rollershutter Living Room', '2/0/1', '2/1/1', '2/2/1',
                                         '2/3/1')
knx_device.add_item(rollershutter)
knx_bridge = ohknx2.KnxBridge('192.168.0.10', 3671, '192.168.0.11')
knx_bridge.add_thing(knx_device)
print(knx_bridge.get_config())