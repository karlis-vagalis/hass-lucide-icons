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
        if (!el || !el.setPaths) {
            return;
        }
        el.clearPaths();

        if (icon.fullCode) {

            console.log("HI BIOZTC")

            await el.updateComplete;
            const root = el.shadowRoot.querySelector("svg");

            root.outerHTML = icon.fullCode;

            /*
            const styleEl = document.createElement("style");
            styleEl.innerHTML = `
          svg:first-child>g:first-of-type>path {
            display: none;
          }
        `;
            root.appendChild(styleEl);
            root.appendChild(icon.fullCode.cloneNode(true));
            */
        } else {
            el.setPaths(icon.paths);
            if (icon.format) {
                el.classList.add(...icon.format.split("-"));
            }
        }
    };
});

customElements.whenDefined("ha-svg-icon").then(() => {
    const HaSvgIcon = customElements.get("ha-svg-icon");

    HaSvgIcon.prototype.clearPaths = async function () {
        await this.updateComplete;

        const svgRoot = this.shadowRoot.querySelector("svg");
        while (svgRoot && svgRoot.children.length > 1)
            svgRoot.removeChild(svgRoot.lastChild);

        const svgGroup = this.shadowRoot.querySelector("g");
        while (svgGroup && svgGroup.children.length > 1)
            svgGroup.removeChild(svgGroup.lastChild);

        while (this.shadowRoot.querySelector("style.fontawesome")) {
            const el = this.shadowRoot.querySelector("style.fontawesome");
            el.parentNode.removeChild(el);
        }
    };

    HaSvgIcon.prototype.setPaths = async function (paths) {
        await this.updateComplete;
        if (paths == undefined || Object.keys(paths).length === 0) return;
        const styleEl =
            this.shadowRoot.querySelector("style.fontawesome") ||
            document.createElement("style");
        styleEl.classList.add("fontawesome");
        styleEl.innerHTML = `
        .secondary {
          opacity: 0.4;
        }
        :host(.invert) .secondary {
          opacity: 1;
        }
        :host(.invert) .primary {
          opacity: 0.4;
        }
        :host(.color) .primary {
          opacity: 1;
        }
        :host(.color) .secondary {
          opacity: 1;
        }
        :host(.color:not(.invert)) .secondary {
          fill: var(--icon-secondary-color, var(--disabled-text-color));
        }
        :host(.color.invert) .primary {
          fill: var(--icon-secondary-color, var(--disabled-text-color));
        }
        path:not(.primary):not(.secondary) {
          opacity: 0;
        }
        `;
        this.shadowRoot.appendChild(styleEl);
        const root = this.shadowRoot.querySelector("g");
        for (const k in paths) {
            const el = document.createElementNS("http://www.w3.org/2000/svg", "path");
            el.setAttribute("d", paths[k]);
            el.classList.add(k);
            root.appendChild(el);
        }
    };
});