from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http.view import HomeAssistantView

import json
from os import walk, path

DOMAIN = "lucide-icons"
SCRIPT_NAME = "main.js"

LOADER_URL = f"/{DOMAIN}/{SCRIPT_NAME}"
ICON_URL = f"/{DOMAIN}/icons"

DATA_EXTRA_MODULE_URL = "frontend_extra_module_url"

class IconListView(HomeAssistantView):

    requires_auth = False

    def __init__(self, url, iconpath):
        self.url = url
        self.iconpath = iconpath
        self.name = "Icon Listing"

    async def get(self, request):
        icons = []
        for (dirpath, dirnames, filenames) in walk(self.iconpath):
            icons.extend(
                [
                    {"name": path.join(dirpath[len(self.iconpath):], fn[:-4])}
                    for fn in filenames if fn.endswith(".svg")
                ]
            )
        return json.dumps(icons)

async def async_setup(hass, config):
    
    # Expose main script which does icon loading on frontend
    hass.http.register_static_path(
        LOADER_URL,
        hass.config.path(f"custom_components/{DOMAIN}/data/{SCRIPT_NAME}"),
        True,
    )
    # Register main script as frontend resource
    add_extra_js_url(hass, LOADER_URL)

    # Exposing icon folder
    hass.http.register_static_path(
        ICON_URL,
        hass.config.path(f"custom_components/{DOMAIN}/data/icons"),
        True,
    )

    # Register icon view, aka list when typing icon name
    hass.http.register_view(
        IconListView(
            f'/{DOMAIN}/list',
            hass.config.path(f"custom_components/{DOMAIN}/data/icons")
        )
    )

    # Return boolean to indicate that initialization was successful.
    return True


async def async_setup_entry(hass, entry):
    return True


async def async_remove_entry(hass, entry):
    return True