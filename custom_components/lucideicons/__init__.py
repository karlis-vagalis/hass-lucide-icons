import homeassistant.components.frontend
from homeassistant.components.frontend import _frontend_root
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.components.http.view import HomeAssistantView

import json

DOMAIN = "lucideicons"
SCRIPT_NAME = "lucide.js"

DATA_EXTRA_MODULE_URL = "frontend_extra_module_url"
ICON_FILES = {DOMAIN: SCRIPT_NAME}
ICONS_URL = "/" + DOMAIN + "/"
ICON_URL = f"/{DOMAIN}/icons"


async def async_setup(hass, config):
    
    hass.http.register_static_path(
        f"/{DOMAIN}/{SCRIPT_NAME}",
        hass.config.path(f"custom_components/{DOMAIN}/data/{SCRIPT_NAME}"),
        True,
    )

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass, config_entry):
    config_entry.add_update_listener(_update_listener)
    register_modules(hass)
    return True


async def async_remove_entry(hass, config_entry):
    register_modules(hass)
    return True


async def _update_listener(hass, config_entry):
    register_modules(hass)
    return True


def register_modules(hass):

    if DATA_EXTRA_MODULE_URL not in hass.data:
        hass.data[DATA_EXTRA_MODULE_URL] = set()
    url_set = hass.data[DATA_EXTRA_MODULE_URL]

    for k, v in ICON_FILES.items():
        url_set.remove(ICONS_URL + v)
        # if k in modules and modules[k] != False:
        url_set.add(ICONS_URL + v)