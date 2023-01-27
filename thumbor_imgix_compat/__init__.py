# -*- coding: utf-8 -*-

# Copyright (c) 2023, Car & Classic

from derpconf.config import Config

from tc_core import Extension, Extensions
from thumbor_imgix_compat.handlers.imgix_compat import ImgxCompatHandler
from thumbor.utils import logger

extension = Extension('thumbor_imgix_compat')

Config.define('IMGIX_COMPAT_HASH', None, 'Imgix hash', 'ImgixCompat')
Config.define('IMGIX_COMPAT_STORAGE_ROOT', None, 'Imgix storage root', 'ImgixCompat')
Config.define('IMGIX_COMPAT_AUTO_QUALITY', 95, 'Quality to use for auto=compress', 'ImgixCompat')

logger.debug("CONFIG")
logger.debug(Config.get("IMGIX_COMPAT_HASH"))

# Register the route
for r in ImgxCompatHandler.regex():
    extension.add_handler(r, ImgxCompatHandler)

Extensions.register(extension)
