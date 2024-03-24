"""Tariff TD."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers import entity_registry as er

from .const import (
    CONF_DIARY_COST,
    CONF_P1,
    CONF_P2,
    CONF_P3,
    CONF_P4,
    CONF_P5,
    CONF_P6,
    CONF_TARIFF,
    TARIFF_20,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up sensors handler."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_options))
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)


async def _async_update_options(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Handle options update."""
    # update entry replacing data with new options
    hass.config_entries.async_update_entry(
        config_entry, data={**config_entry.data, **config_entry.options}
    )
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migration scripts."""
    version = config_entry.version

    if version == 1:
        data = {
            CONF_P4: 0.0,
            CONF_P5: 0.0,
            CONF_P6: 0.0,
            CONF_TARIFF: TARIFF_20,
            CONF_P1: config_entry.data["precio_punta"],
            CONF_P2: config_entry.data["precio_llana"],
            CONF_P3: config_entry.data["precio_valle"],
            CONF_DIARY_COST: config_entry.data["coste_dia"],
        }

        hass.config_entries.async_update_entry(config_entry, data=data)

        def _async_migrator(entity_entry: er.RegistryEntry) -> dict[str, str]:
            old_unique_id = entity_entry.unique_id
            new_unique_id = f"{entity_entry.config_entry_id}-{old_unique_id}"
            _LOGGER.debug(
                "Updating unique_id from %s to %s", old_unique_id, new_unique_id
            )
            return {"new_unique_id": new_unique_id}

        await er.async_migrate_entries(hass, config_entry.entry_id, _async_migrator)
        config_entry.version = 3

    return True
