from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorMode,
    NumberSelectorConfig,
)


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("precio_valle"): NumberSelector(
            NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh", mode=NumberSelectorMode.BOX)
        ),
        vol.Required("precio_llana"): NumberSelector(
            NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh", mode=NumberSelectorMode.BOX)
        ),
        vol.Required("precio_punta"): NumberSelector(
            NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh", mode=NumberSelectorMode.BOX)
        ),
        vol.Required("coste_dia"): NumberSelector(
            NumberSelectorConfig(min=0, max=3, step="any", unit_of_measurement="€/dia", mode=NumberSelectorMode.BOX)
        )
    }
)


class PlaceholderHub:
    def __init__(self, precio_valle: float, precio_llana: float, precio_punta: float, coste_dia: float) -> None:
        """Initialize."""
        self.precio_valle = precio_valle
        self.precio_llana = precio_llana
        self.precio_punta = precio_punta
        self.coste_dia = coste_dia


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )
        else:
            return self.async_create_entry(title="", data=user_input)
