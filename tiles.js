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
  cam1:          false,   // ferry cam (live video, iframe)
  roofwind:      true,   // Ecowitt roof wind meter
  windmap:       true,   // animated wind map
<<<<<<< Updated upstream
  cam2:          true,   // Kaag cam
  pv:            false,   // solar production (dummy data) 
  marinetraffic: false,  // AIS ship map
=======
  cam2:          true,   // Kaag cam (live video, iframe)
  pv:            false,   // solar production (dummy data)
  marinetraffic: false,  // AIS ship map
  "cam1-snap":   true,  // ferry cam, snapshot version (lighter on the Pi than cam1)
  "cam2-snap":   false,  // Kaag cam, snapshot version (lighter on the Pi than cam2)
>>>>>>> Stashed changes
};
