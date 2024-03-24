"""Create and update configuration flows."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, override

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
)

from .const import (
    CONF_DIARY_COST,
    CONF_P1,
    CONF_P2,
    CONF_P3,
    CONF_P4,
    CONF_P5,
    CONF_P6,
    CONF_TARIFF,
    DOMAIN,
    TARIFF_20,
    TARIFF_30,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.data_entry_flow import FlowResult

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Tariff TD."""

    VERSION = 2
    tariff = TARIFF_20

    @staticmethod
    @callback
    @override
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionFlowHandler:
        return OptionFlowHandler(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Config flow of Tariff TD."""
        if user_input is not None:
            self.tariff = user_input[CONF_TARIFF]
            if self.tariff == TARIFF_30:
                return await self.async_step_tariff30()

            return await self.async_step_tariff20()

        schema = vol.Schema(
            {
                vol.Required(CONF_TARIFF): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(
                                value=TARIFF_20, label="Tarifa 2.0 TD (3 periodos)"
                            ),
                            SelectOptionDict(
                                value=TARIFF_30, label="Tarifa 3.0 TD (6 periodos)"
                            ),
                        ]
                    )
                )
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_tariff20(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Form configuration for Tariff 2.0 TD."""
        if user_input is not None:
            user_input[CONF_TARIFF] = self.tariff
            return self.async_create_entry(data=user_input, title="Tarifa TD")

        schema = {
            vol.Required(CONF_DIARY_COST): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    step="any",
                    unit_of_measurement="€",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P1): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P2): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P3): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
        }

        return self.async_show_form(step_id="tariff20", data_schema=vol.Schema(schema))

    async def async_step_tariff30(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Form configuration for Tariff 3.0 TD."""
        if user_input is not None:
            user_input[CONF_TARIFF] = self.tariff
            return self.async_create_entry(data=user_input, title="Tarifa TD")

        schema = {
            vol.Required(CONF_DIARY_COST): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    step="any",
                    unit_of_measurement="€",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P1): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P2): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P3): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P4): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P5): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P6): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
        }

        return self.async_show_form(step_id="tariff30", data_schema=vol.Schema(schema))


class OptionFlowHandler(config_entries.OptionsFlow):
    """Reconfigure Flow for Tariff TD."""

    tariff = TARIFF_20

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialise values."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Tariff TD selector form."""
        if user_input is not None:
            self.tariff = user_input[CONF_TARIFF]
            if self.tariff == TARIFF_30:
                return await self.async_step_tariff30()

            return await self.async_step_tariff20()

        tariff = self.config_entry.data.get(CONF_TARIFF, TARIFF_20)

        schema = vol.Schema(
            {
                vol.Required(CONF_TARIFF, default=tariff): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(
                                value=TARIFF_20, label="Tarifa 2.0 TD (3 periodos)"
                            ),
                            SelectOptionDict(
                                value=TARIFF_30, label="Tarifa 3.0 TD (6 periodos)"
                            ),
                        ]
                    )
                )
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)

    async def async_step_tariff20(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Form configuration for Tariff 2.0 TD."""
        if user_input is not None:
            user_input[CONF_TARIFF] = self.tariff
            return self.async_create_entry(data=user_input, title="Tarifa TD")

        p1 = self.config_entry.data.get(CONF_P1, 0)
        p2 = self.config_entry.data.get(CONF_P2, 0)
        p3 = self.config_entry.data.get(CONF_P3, 0)
        diary = self.config_entry.data.get(CONF_DIARY_COST, 0)

        schema = {
            vol.Required(CONF_DIARY_COST, default=diary): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    step="any",
                    unit_of_measurement="€",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P1, default=p1): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P2, default=p2): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P3, default=p3): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
        }

        return self.async_show_form(step_id="tariff20", data_schema=vol.Schema(schema))

    async def async_step_tariff30(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Form configuration for Tariff 3.0 TD."""
        if user_input is not None:
            user_input[CONF_TARIFF] = self.tariff
            return self.async_create_entry(data=user_input, title="Tarifa TD")

        p1 = self.config_entry.data.get(CONF_P1, 0)
        p2 = self.config_entry.data.get(CONF_P2, 0)
        p3 = self.config_entry.data.get(CONF_P3, 0)
        p4 = self.config_entry.data.get(CONF_P4, 0)
        p5 = self.config_entry.data.get(CONF_P5, 0)
        p6 = self.config_entry.data.get(CONF_P6, 0)
        diary = self.config_entry.data.get(CONF_DIARY_COST, 0)

        schema = {
            vol.Required(CONF_DIARY_COST, default=diary): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    step="any",
                    unit_of_measurement="€",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P1, default=p1): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P2, default=p2): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P3, default=p3): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P4, default=p4): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P5, default=p5): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
            vol.Required(CONF_P6, default=p6): NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=1,
                    step="any",
                    unit_of_measurement="€/kWh",
                    mode=NumberSelectorMode.BOX,
                )
            ),
        }

        return self.async_show_form(step_id="tariff30", data_schema=vol.Schema(schema))
