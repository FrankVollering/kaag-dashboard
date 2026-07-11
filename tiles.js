// ============================================================
// Dashboard tile switchboard — edit freely.
// true  = tile is shown
// false = tile is hidden (its iframes are also unloaded)
// The order of the lines below is also the display order
// on the dashboard (left to right, top to bottom).
// ============================================================
const TILES = {
  weather:       true,   // forecast + temperature chart
  buienradar:    true,   // rain radar
  cam1:          true,   // ferry cam
  roofwind:      true,   // Ecowitt roof wind meter
  windmap:       true,   // animated wind map
  cam2:          true,   // Kaag cam
  pv:            true,   // solar production (dummy data) 
  marinetraffic: true,  // AIS ship map
};
