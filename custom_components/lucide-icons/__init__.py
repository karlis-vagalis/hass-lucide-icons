from homeassistant.components.frontend import add_extra_js_url

DOMAIN = "lucide-icons"
SCRIPT_NAME = "main.js"

LOADER_URL = f"/{DOMAIN}/{SCRIPT_NAME}"
ICON_URL = f"/{DOMAIN}/icons"

DATA_EXTRA_MODULE_URL = "frontend_extra_module_url"

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

    # Return boolean to indicate that initialization was successful.
    return True


async def async_setup_entry(hass, entry):
    return True


async def async_remove_entry(hass, entry):
    return True