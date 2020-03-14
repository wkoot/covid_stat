var mapOpts = {
    style: 'grijs',
    target: 'map',
    center: {
        longitude: 5.35,
        latitude: 52.15
    },
    overlay: 'false',
    marker: false,
    zoom: 8,
    search: false
};

var lineStyle = {
    "color": "#aaa",
    "weight": 1,
    "opacity": 0.3
};

var defaultFillOpacity = 0.3;

function getPctColorStyle(gemeente_obj, gemeente_props) {
    var value = (gemeente_obj["count"] / gemeente_props["inwoners"]) * 18000;
    var colorValue;

    if (value === undefined || value === "" || value < 0.5)
        colorValue = "#f5faeb";
    else if (value < 1)
        colorValue = "#cbd5cf";
    else if (value < 2)
        colorValue = "#a1b1b4";
    else if (value < 5)
        colorValue = "#768c98";
    else if (value < 10)
        colorValue = "#4c687d";
    else
        colorValue = "#224361";

    return {"fillColor": colorValue, "fillOpacity": defaultFillOpacity};
}

function getAbsColorStyle(gemeente_obj) {
    var value = gemeente_obj["count"];
    var colorValue;

    if (value === undefined || value === "" || value < 2)
        colorValue = "#f5faeb";
    else if (value < 4)
        colorValue = "#cbd5cf";
    else if (value < 7)
        colorValue = "#a1b1b4";
    else if (value < 12)
        colorValue = "#768c98";
    else if (value < 25)
        colorValue = "#4c687d";
    else
        colorValue = "#224361";

    return {"fillColor": colorValue, "fillOpacity": defaultFillOpacity};
}

function getNewColorStyle(gemeente_obj) {
    var value = gemeente_obj["increase"];
    var colorValue;

    if (value === undefined || value === "" || value < 1)
        colorValue = "#f5faeb";
    else if (value < 2)
        colorValue = "#cbd5cf";
    else if (value < 4)
        colorValue = "#a1b1b4";
    else if (value < 7)
        colorValue = "#768c98";
    else if (value < 10)
        colorValue = "#4c687d";
    else
        colorValue = "#224361";

    return {"fillColor": colorValue, "fillOpacity": defaultFillOpacity};
}

function getDensColorStyle(gemeente_obj, gemeente_props) {
    var value = (gemeente_obj["count"] / gemeente_props["land_oppervlak"]) * 40;
    var colorValue;

    if (value === undefined || value === "" || value < 1)
        colorValue = "#f5faeb";
    else if (value < 2)
        colorValue = "#cbd5cf";
    else if (value < 4)
        colorValue = "#a1b1b4";
    else if (value < 7)
        colorValue = "#768c98";
    else if (value < 10)
        colorValue = "#4c687d";
    else
        colorValue = "#224361";

    return {"fillColor": colorValue, "fillOpacity": defaultFillOpacity};
}
