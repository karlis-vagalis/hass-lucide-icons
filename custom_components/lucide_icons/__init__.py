import json
import logging
from os import path, walk
from xml.etree import ElementTree

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.helpers import config_validation
from homeassistant.helpers.http import HomeAssistantView
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "lucide_icons"
SCRIPT_NAME = "main.js"

FRONTEND_SCRIPT_URL = f"/{DOMAIN}/{SCRIPT_NAME}"
ICON_URL = f"/{DOMAIN}/icons"
LIST_URL = f"/{DOMAIN}/list"

DATA_EXTRA_MODULE_URL = "frontend_extra_module_url"
CONFIG_SCHEMA = config_validation.empty_config_schema(DOMAIN)


class IconListView(HomeAssistantView):
    url = LIST_URL
    requires_auth = False

    def __init__(self, hass: HomeAssistant):
        self._hass = hass
        self._icon_dir = hass.config.path(f"custom_components/{DOMAIN}/data/icons")

    def _get_icons(self):
        icons = []
        for root, dirs, files in walk(self._icon_dir):
            for file in files:
                if file.endswith(".svg"):
                    name = file[:-4]
                    svg = ElementTree.parse(path.join(root, file)).getroot()
                    keywords = []
                    if "tags" in svg.attrib:
                        keywords = svg.attrib["tags"].split(",")
                    icons.append({"name": name, "keywords": keywords})
        return icons

    async def get(self, request):
        icons = await self._hass.async_add_executor_job(self._get_icons)
        return json.dumps(icons)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # Expose main script which does icon loading on frontend and icon folder
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                FRONTEND_SCRIPT_URL,
                hass.config.path(f"custom_components/{DOMAIN}/data/{SCRIPT_NAME}"),
                True,
            ),
            StaticPathConfig(
                ICON_URL,
                hass.config.path(f"custom_components/{DOMAIN}/data/icons"),
                True,
            ),
        ]
    )
    # Register main script as frontend resource
    add_extra_js_url(hass, FRONTEND_SCRIPT_URL)

    # Register icon view, aka list when typing icon name
    hass.http.register_view(IconListView(hass))

    # Return boolean to indicate that initialization was successful.
    return True


async def async_setup_entry(hass, entry):
    return True


async def async_remove_entry(hass, entry):
    return True
