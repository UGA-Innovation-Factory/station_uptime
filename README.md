# station_uptime - Home Assistant Custom Component
### This component is for displaying the uptime of a station in Home Assistant.

## Installation
1. Copy the `station_uptime` folder into your `custom_components` folder.
2. Add the following to your `configuration.yaml` file:
    ```yaml
    station_uptime:
      stations:
        - name: station_1 # Your stations here
    ```
3. Restart Home Assistant.

## Usage
Stations are interfaced with via HomeAssistant services
### Services
- `station_uptime.start_assembly` - Starts the uptime counter for a station
    - `station_id` - The name of the station to start the counter for
- `station_uptime.finish_assembly` - Stops the uptime counter for a station
    - `station_id` - The name of the station to stop the counter for

## Example
   ```yaml
   service: station_uptime.start_assembly
   data:
     entity_id: station_uptime.station_1
   ```