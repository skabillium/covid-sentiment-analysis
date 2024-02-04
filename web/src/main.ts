import 'leaflet/dist/leaflet.css';
import './style.css';

import L from 'leaflet';
import tweets from './tweets.json';
import { Feature, GeoJsonObject, Geometry } from 'geojson';

type TweetFeatureProperties = {
  ADMIN: string;
  ISO_A3: string;
  greekName: string;
  flagUrl: string;
  positivePct: number;
  neutralPct: number;
  negativePct: number;
  tweets: number;
  vaccineCoverage: number;
};

type TweetFeature = Feature<Geometry, TweetFeatureProperties> | undefined;

/**
 * Maps positive percentage ranges to colors on the map
 */
const ColorPallete = {
  LT_10: '#92013A',
  LT_15: '#C52A52',
  LT_20: '#e75d6e',
  LT_25: '#FD9291',
  LT_30: '#FFCAB9',
  LT_35: '#B0DFDB',
  LT_40: '#85B7CD',
  LT_45: '#618FBF',
  LT_50: '#3D67AE',
  GTE_50: '#00429C',
};

/**
 * Get the default style for country
 * @param feature Country tweets geojson feature
 */
function getFeatureStyle(feature: TweetFeature) {
  const positive = feature?.properties.positivePct!;
  let fillColor: string;

  switch (true) {
    case positive < 10:
      fillColor = ColorPallete.LT_10;
      break;
    case positive >= 10 && positive < 15:
      fillColor = ColorPallete.LT_15;
      break;
    case positive >= 15 && positive < 20:
      fillColor = ColorPallete.LT_20;
      break;
    case positive >= 20 && positive < 25:
      fillColor = ColorPallete.LT_25;
      break;
    case positive >= 25 && positive < 30:
      fillColor = ColorPallete.LT_30;
      break;
    case positive >= 30 && positive < 35:
      fillColor = ColorPallete.LT_35;
      break;
    case positive >= 35 && positive < 40:
      fillColor = ColorPallete.LT_40;
      break;
    case positive >= 40 && positive < 45:
      fillColor = ColorPallete.LT_45;
      break;
    case positive >= 45 && positive < 50:
      fillColor = ColorPallete.LT_50;
      break;
    default:
      fillColor = ColorPallete.GTE_50;
  }

  return {
    color: 'black',
    fillOpacity: 0.7,
    weight: 0.25,
    fillColor,
  };
}

const map = L.map('map').setView([30, 0], 2.7);

L.tileLayer(
  'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png',
  {
    attribution:
      '\u0026copy; \u003ca target="_blank" href="http://www.openstreetmap.org/copyright"\u003eOpenStreetMap\u003c/a\u003e contributors \u0026copy; \u003ca target="_blank" href="http://cartodb.com/attributions"\u003eCartoDB\u003c/a\u003e, CartoDB \u003ca target="_blank" href ="http://cartodb.com/attributions"\u003eattributions\u003c/a\u003e',
    detectRetina: false,
    maxNativeZoom: 18,
    // maxZoom: 18,
    minZoom: 2.0,
    noWrap: false,
    opacity: 1,
    subdomains: 'abc',
    tms: false,
  },
).addTo(map);

const geojson = L.geoJSON<TweetFeatureProperties>(tweets as GeoJsonObject, {
  onEachFeature(feature, layer) {
    layer.on({
      mouseout(event) {
        const style = getFeatureStyle(feature);
        event.target.setStyle(style);
      },
      mouseover(event) {
        // Hightlight feature on hover
        const highlightedStyle = {
          color: 'green',
          fillColor: '#40bc74',
          weight: 2,
        };
        event.target.setStyle(highlightedStyle);
      },
    });
  },
  style: getFeatureStyle,
}).addTo(map);

geojson.on('click', (event) => {
  const feature = event.propagatedFrom.feature as TweetFeature;
  const { properties } = feature!;

  L.tooltip({ permanent: false })
    .setContent(
      `<div style="font-weight: bold; font-size: 1.2em" >${properties.greekName}</div>
    <div>Κάλυψη: ${properties.vaccineCoverage ? properties.vaccineCoverage+ '%':'Άγνωστο' }</div>
    <div>Tweets: ${properties.tweets}</div>
    <div>Θετικά: ${properties.positivePct}%</div>
    <div>Ουδέτερα: ${properties.neutralPct}%</div>
    <div>Αρνητικά: ${properties.negativePct}%</div>
    `,
    )
    .setLatLng(event.latlng)
    .addTo(map);
});

const LegendControl = L.Control.extend({
  options: {
    position: 'bottomleft',
  },
  onAdd() {
    const legendDiv = L.DomUtil.create('div');
    legendDiv.style.backgroundColor = 'white';
    legendDiv.style.padding = '10px';
    legendDiv.style.paddingTop = '1px';
    legendDiv.style.borderRadius = '10px';

    // TODO: Maybe put these in a template
    legendDiv.innerHTML = `
    <div style="font-weight: bold; font-size: 1.3em; margin-bottom: 5px; padding: 10px;">%Θετικών</div>
    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_10}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>0-9</span>
    </div>
    
    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_15}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>10-14</span>
    </div> 

    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_20}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>15-19</span>
    </div> 

    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_25}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>20-24</span>
    </div> 

    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_30}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>25-29</span>
    </div> 

    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_35}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>30-34</span>
    </div> 

    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_40}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>35-39</span>
    </div> 

    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_45}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>40-44</span>
    </div> 

    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.LT_50}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>45-49</span>
    </div> 

    <div style="margin-bottom: 5px;">
    <span style="background-color: ${ColorPallete.GTE_50}; width: 10px; height: 10px; display: inline-block;"></span>
    <span>>=50</span>
    </div> 
    `;

    return legendDiv;
  },
});

const legend = new LegendControl();
legend.addTo(map);
