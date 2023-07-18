import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.core import HomeAssistant, callback
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

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_STATIONS): vol.All(cv.ensure_list, [STATION_SCHEMA]),
    }
)


async def async_setup_platform(hass: HomeAssistant, config: dict, async_add_entities, discovery_info=None):
    stations = config.get(CONF_STATIONS)

    entities = []
    for station in stations:
        entity = BinarySensorEntity(station[CONF_NAME])
        entities.append(entity)

    async_add_entities(entities)

    async def async_start_assembly(call):
        entity_id = call.data["entity_id"]
        entity_obj = hass.states.get(entity_id)
        hass.states.async_set(entity_id, 'on', entity_obj.attributes)

    async def async_finish_assembly(call):
        entity_id = call.data["entity_id"]
        entity_obj = hass.states.get(entity_id)
        hass.states.async_set(entity_id, 'off', entity_obj.attributes)

    hass.services.async_register(
        DOMAIN, "start_assembly", async_start_assembly, schema=vol.Schema({vol.Required("entity_id"): cv.string})
    )
    hass.services.async_register(
        DOMAIN, "finish_assembly", async_finish_assembly, schema=vol.Schema({vol.Required("entity_id"): cv.string})
    )

    return True
