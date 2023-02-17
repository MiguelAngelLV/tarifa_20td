"""Balance Neto"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_options))
    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    # update entry replacing data with modified options
    hass.config_entries.async_update_entry(
        entry, data={**entry.data, **entry.options}
    )
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_update_options(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Handle options update."""
    # update entry replacing data with new options
    hass.config_entries.async_update_entry(
        config_entry, data={**config_entry.data, **config_entry.options}
    )
    await hass.config_entries.async_reload(config_entry.entry_id)