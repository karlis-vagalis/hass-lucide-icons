import "https://unpkg.com/lucide@latest";

async function getIcon(name) {

    name = transformName(name);

    let icon = lucide[name]

    //console.log(icon);

    if (icon === undefined) {
        return;
    }

    var fullCode = generateFullCode(icon);

    //console.log(fullCode);
    
    var o = {
        "fullCode": fullCode,
        "path": "",
        "viewBox": icon[1].viewBox,
    };

    return o;
}

async function getIconList() {
    return {};
}

function generateFullCode (icon) {

    var params = icon[1];
    var data = icon[2];

    data = data.map((e) => {
        var type = e[0]

        var defs = []
        Object.keys(e[1]).forEach(function(key,index) {
            defs.push(`${key}="${e[1][key]}"`);
        });

        return `<${type} ${defs.join(" ")}></${type}>`
    })

    return `<svg xmlns="${params.xmlns}" width="${params.width}" height="${params.height}" viewBox="${params.viewBox}" fill="${params.fill}" stroke="${params.stroke}" stroke-width="${params["stroke-width"]}" stroke-linecap="${params["stroke-linecap"]}" stroke-linejoin="${params["stroke-linejoin"]}">${data.join("")}</svg>`;
}

function transformName(name) {
    var parts = name.split('-');
    parts = parts.map((x) => {
        return x.charAt(0).toUpperCase() + x.slice(1);
    })
    return parts.join("");
}

window.customIcons = window.customIcons || {};
window.customIcons["lucide"] = { getIcon, getIconList };



// FontAwesome icopns https://github.com/thomasloven/hass-fontawesome/blob/master/js/main.js

customElements.whenDefined("ha-icon").then(() => {

    const HaIcon = customElements.get("ha-icon");

    HaIcon.prototype._setCustomPath = async function (promise, requestedIcon) {

        const icon = await promise;

        if (requestedIcon !== this.icon || icon === undefined) return;
        this._path = icon.path;
        this._viewBox = icon.viewBox;

        await this.UpdateComplete;

        const el = this.shadowRoot.querySelector("ha-svg-icon");
        const root = el.shadowRoot;

        //console.log(root);

        root.innerHTML = icon.fullCode;

    };
});