from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

hammy = hal.backend.devices["Hamilton"]
hammy.start()

cent = hal.centrifuge.devices["Hig4"]

cent.initialize()

cent.close()

cent.spin(2000,100,100)

import time

time.sleep(20)


cent.stop()

cent.select_bucket(1)


input("ENTER")
hammy.stop()