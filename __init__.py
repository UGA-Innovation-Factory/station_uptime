import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components.binary_sensor import BinarySensorEntity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "station_uptime"

CONF_STATIONS = "stations"

STATION_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_STATIONS): vol.All(cv.ensure_list, [STATION_SCHEMA]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


class StationUptimeEntity(BinarySensorEntity):
    def __init__(self, name):
        self._is_on = False
        self._attr_name = name
        self._attr_unique_id = name
        self._attr_icon = "mdi:hammer-screwdriver"
        self._attr_should_poll = False

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def start_assembly(self):
        self._is_on = True
        self.schedule_update_ha_state(True)

    def finish_assembly(self):
        self._is_on = False
        self.schedule_update_ha_state(True)


async def async_setup(hass: HomeAssistant, config: dict):
    stations = config[DOMAIN].get(CONF_STATIONS)
    component = EntityComponent(_LOGGER, DOMAIN, hass)

    entities = []
    for station in stations:
        entity = StationUptimeEntity(station[CONF_NAME])
        entities.append(entity)

    await component.async_add_entities(entities)

    async def async_start_assembly(call):
        entity_id = call.data["entity_id"]
        entity_obj = component.get_entity(entity_id)
        entity_obj.start_assembly()
        entity_obj.async_write_ha_state()


    async def async_finish_assembly(call):
        entity_id = call.data["entity_id"]
        entity_obj = component.get_entity(entity_id)
        entity_obj.finish_assembly()
        entity_obj.async_write_ha_state()

    hass.services.async_register(
        DOMAIN, "start_assembly", async_start_assembly, schema=vol.Schema({vol.Required("entity_id"): cv.string})
    )
    hass.services.async_register(
        DOMAIN, "finish_assembly", async_finish_assembly, schema=vol.Schema({vol.Required("entity_id"): cv.string})
    )

    return True
