from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.core import callback

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorMode,
    NumberSelectorConfig,
)

from .const import *

_LOGGER = logging.getLogger(__name__)

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_VALLE): NumberSelector(
            NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh", mode=NumberSelectorMode.BOX)
        ),
        vol.Required(CONF_LLANA): NumberSelector(
            NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh", mode=NumberSelectorMode.BOX)
        ),
        vol.Required(CONF_PUNTA): NumberSelector(
            NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh", mode=NumberSelectorMode.BOX)
        ),
        vol.Required(CONF_DIA): NumberSelector(
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

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionFlowHandler(config_entry)

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=SCHEMA
            )
        else:
            return self.async_create_entry(title="Tarifa 2.0 TD", data=user_input)


class OptionFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="Tarifa 2.0 TD", data=user_input)

        # Fill options with entry data
        valle = self.config_entry.options.get(
            CONF_VALLE, self.config_entry.data[CONF_VALLE]
        )
        llana = self.config_entry.options.get(
            CONF_LLANA, self.config_entry.data[CONF_LLANA]
        )
        punta = self.config_entry.options.get(
            CONF_PUNTA, self.config_entry.data[CONF_PUNTA]
        )
        dia = self.config_entry.options.get(
            CONF_DIA, self.config_entry.data[CONF_DIA]
        )

        schema = vol.Schema(
            {
                vol.Required(CONF_VALLE, default=float(valle)): NumberSelector(
                    NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh",
                                         mode=NumberSelectorMode.BOX)
                ),
                vol.Required(CONF_LLANA, default=float(llana)): NumberSelector(
                    NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh",
                                         mode=NumberSelectorMode.BOX)
                ),
                vol.Required(CONF_PUNTA, default=float(punta)): NumberSelector(
                    NumberSelectorConfig(min=0, max=1, step="any", unit_of_measurement="€/kWh",
                                         mode=NumberSelectorMode.BOX)
                ),
                vol.Required(CONF_DIA, default=float(dia)): NumberSelector(
                    NumberSelectorConfig(min=0, max=3, step="any", unit_of_measurement="€/dia",
                                         mode=NumberSelectorMode.BOX)
                )
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
