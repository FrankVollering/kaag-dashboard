// ============================================================
// Dashboard tile switchboard — edit freely.
// true  = tile is shown
// false = tile is hidden (its iframes are also unloaded)
// The order of the lines below is also the display order
// on the dashboard (left to right, top to bottom).
// ============================================================
const TILES = {
  weather:       true,   // forecast + temperature chart
  roofwind:      true,   // Ecowitt roof wind meter
  cam1:          false,   // ferry cam (live video, iframe)
  "cam1-snap":   true,  // ferry cam, snapshot version (lighter on the Pi than cam1)
  windmap:       true,   // animated wind map
  buienradar:    true,   // rain radar
  cam2:          false,   // Kaag cam (live video, iframe)
  "cam2-snap":   true,  // Kaag cam, snapshot version (lighter on the Pi than cam2)
  pv:            false,   // solar production (dummy data)
  marinetraffic: false,  // AIS ship map
};
