# hass-lucide-icons

This is custom component/integration enables the usage of the awesome [Lucide](https://lucide.dev/) icon pack.

Huge thanks to *Thomas Lovén* and his custom component [hass-fontawesome](https://github.com/thomasloven/hass-fontawesome), which helped me a lot to develop this icon set integration.

## Installation

### HACS

See [#5072](https://github.com/home-assistant/brands/pull/5072)

To install via HACS add this repository as `Custom Repository` in HACS. Then search for `Lucide icons`. Install.

### Manual

1. Copy `lucide_icons` folder to your custom components.
2. Restart Home Assistant
3. Install `Lucide Icons` component under Home Assistant > Integrations
4. Restart Home Assistant

## Usage

This icon pack uses prefix `lucide` to access icons. For example:
```
lucide:trash

lucide:circle-dot

...
```

## Features

This icon pack integration also supports icon keywords, which means you can use keywords/aliases of the icons to search icons inside the native Home Assistant icon dialog. For example, icon `cpu` has additional aliases/keywords and one of them is `processor`. Therefore we may type `processor` in icon search bar in Home Assistant and voila, the correct icon is suggested as seen here:

![keywords example](./docs/images/keywords.png)
