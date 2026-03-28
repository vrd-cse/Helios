// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('helios');

// Create a new document in the collection.
db.energy.insertMany(
    [
        {
  "timestamp": "2024-01-01T00:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.7,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T01:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.5,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T02:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.3,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T03:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T04:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T05:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T06:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 20,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T07:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 50,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T08:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 110,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T09:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 155,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T010:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 445,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T11:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 598,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T12:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 750,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T13:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 886,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T14:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 965,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T15:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 871,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T16:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 662,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T17:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 432,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T18:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 198,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T19:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 78,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T20:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T21:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T22:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
{
  "timestamp": "2024-01-01T23:00:00Z",
  "solar_generation_mw": 0,
  "solar_irradiance_wm2": 0,
  "temperature_c": 17.8,
  "cloud_cover": 0.42,
  "panel_efficiency": 0.20,
  "energy_demand_mw": 168,
  "battery_storage_mwh": 300,
  "grid_export_mw": 0
},
    
    
]);
