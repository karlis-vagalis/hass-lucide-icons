const DOMAIN = "lucide-icons";

// Icon store to store already fetched and loaded icons
const ICONS = {};

async function getIcon(name) {

    let icon = undefined;

    if (ICONS[name] !== undefined) {
        icon = ICONS[name];
    } else {
        const response = await fetch(`/${DOMAIN}/icons/${name}.svg`);

        if (!response.ok) return {};
        icon = await response.text();
        icon = extractPath(icon);
        ICONS[name] = icon;
    }
    
    return {
        "path": icon,
        "viewBox": "0 0 24 24",
    };
}

async function getIconList() {
    const data = await fetch(`/${DOMAIN}/list`);
    const text = await data.text();
    return JSON.parse(text);
}

function extractPath(svg) {
    var tmp = document.createElement('div');
    tmp.innerHTML = svg;
    var d = tmp.querySelector("svg").querySelector("path").getAttribute("d");
    return d;
}

window.customIcons = window.customIcons || {};
window.customIcons["lucide"] = { getIcon, getIconList };

window.customIconsets = window.customIconsets || {};
window.customIconsets["lucide"] = getIcon;

console.info(
    `%c lucide-icons %c | Version v1.0 `,
    "color: white; font-weight: bold; background: #FF4F00",
    "color: white; font-weight: bold; background: #FF4F00",
);