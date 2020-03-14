function zoomToFeature(event) {
    var layer = event.target;
    map.fitBounds(layer.getBounds());
}

function resetHighlight(event) {
    var layer = event.target;
    layer.setStyle({fillOpacity: 0.3});
    layer.closeTooltip();
}

function highlightFeature(event) {
    var layer = event.target;
    layer.setStyle({fillOpacity: 0.6});
    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
    layer.openTooltip();
}

function onEachFeatureBase(feature, layer, gemeente_obj, gemeente_props) {

    var details = "<dl>" +
        "<dt>" + feature.properties['Gemeentena'] + "</dt>" +
        "<dd>Inwoners: " + feature.properties['inwoners'].toLocaleString() + "</dd>" +
        "<dd>Landoppervlak: " + feature.properties['land_oppervlak'].toLocaleString() + " km²</dd>" +
        "<dd>Bevolkinsdichtheid: " + feature.properties['bevolkinsdichtheid'].toLocaleString() + " per km²</dd>" +
        "<dd>Totaal besmettingen: " + gemeente_obj['count'].toLocaleString() + "</dd>" +
        "<dd>Nieuwe besmettingen: " + gemeente_obj['increase'].toLocaleString() + "</dd>" +
        "<dd>Besmettingspercentage: " + (gemeente_obj["count"] * 100 / gemeente_props["inwoners"]).toLocaleString() + "</dd>" +
        "<dd>Besmettingen per km²: " + (gemeente_obj["count"] / gemeente_props["land_oppervlak"]).toLocaleString() + "</dd>" +
        "</dl>";
    layer.bindTooltip(details);

    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}
