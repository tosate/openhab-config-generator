import ohknx2


knx_device = ohknx2.KnxThing('generic', '1.1.1')
knx_bridge = ohknx2.KnxBridge('192.168.0.10', 3671, '192.168.0.11')
knx_bridge.add_thing(knx_device)
print(knx_bridge.get_config())