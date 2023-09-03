from typing import Mapping, Any
from datetime import datetime, timedelta

import holidays

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    DEVICE_CLASS_MONETARY,
    STATE_CLASS_TOTAL_INCREASING,
    DEVICE_CLASS_ENERGY,
    RestoreEntity
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.event import async_track_point_in_time

PRICE_DESCRIPTION = SensorEntityDescription(
    key="precio_20td",
    icon="mdi:currency-eur",
    name="Precio kWh",
    device_class=DEVICE_CLASS_MONETARY,
    native_unit_of_measurement="€/kWh"
)

FIXED_DESCRIPTION = SensorEntityDescription(
    key="coste_fijo_20td",
    icon="mdi:currency-eur",
    name="Costes Fijos Totales",
    state_class=STATE_CLASS_TOTAL_INCREASING,
    native_unit_of_measurement="€"
)

DUMMY_DESCRIPTION = SensorEntityDescription(
    key="coste_fijo_kwh",
    icon="mdi:currency-eur",
    name="Costes Fijos",
    device_class=DEVICE_CLASS_ENERGY,
    state_class=STATE_CLASS_TOTAL_INCREASING,
    native_unit_of_measurement="kWh"
)


async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    valle = float(entry.data['precio_valle'])
    llana = float(entry.data['precio_llana'])
    punta = float(entry.data['precio_punta'])
    coste_dia = float(entry.data['coste_dia'])

    price_sensor = PriceSensor(PRICE_DESCRIPTION, valle, llana, punta, hass)
    fixed_sensor = FixedSensor(FIXED_DESCRIPTION, coste_dia, hass)
    dummy_sensor = DummySensor(DUMMY_DESCRIPTION)
    async_add_entities([price_sensor, fixed_sensor, dummy_sensor])


class PriceSensor(SensorEntity):

    def __init__(self, description: SensorEntityDescription, valle: float, llana: float, punta: float, hass) -> None:
        super().__init__()
        self._state = None
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = description.key
        self.entity_description = description
        self._valle = valle
        self._llana = llana
        self._punta = punta
        self._period = ''
        self._holidays = holidays.ES()
        async def update_price_and_schedule(now):
            self.update_price()
            next = now + timedelta(hours=1)
            async_track_point_in_time(hass, update_price_and_schedule, next)

        now = datetime.now()
        next = now.replace(minute=0, second=0) + timedelta(hours=1)
        async_track_point_in_time(hass, update_price_and_schedule, next)

    @property
    def native_value(self) -> StateType:
        return self._state

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return {'Period': self._period}

    async def async_added_to_hass(self) -> None:
        self.update_price()

    @property
    def should_poll(self):
        return False

    def update_price(self):
        now = datetime.now()

        if now in self._holidays or 5 <= now.weekday() <= 6:
            self._state = self._valle
            self._period = 'P3'
        else:
            hour = now.hour
            if hour < 8:
                self._state = self._valle
                self._period = 'P3'
            elif hour < 10:
                self._state = self._llana
                self._period = 'P2'
            elif hour < 14:
                self._state = self._punta
                self._period = 'P1'
            elif hour < 18:
                self._state = self._llana
                self._period = 'P2'
            elif hour < 22:
                self._state = self._punta
                self._period = 'P3'
            else:
                self._state = self._llana
                self._period = 'P2'

        self.async_write_ha_state()


class FixedSensor(SensorEntity, RestoreEntity):

    def __init__(self, description: SensorEntityDescription, coste_dia, hass) -> None:
        super().__init__()
        self._state = 0
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = description.key
        self.entity_description = description
        self._coste_dia = coste_dia

        async def update_cost_and_schedule(now):
            self.update_price()
            next = now + timedelta(days=1)
            async_track_point_in_time(hass, update_cost_and_schedule, next)

        now = datetime.now()
        next = now.replace(hour=0, minute=5, second=0) + timedelta(days=1)
        async_track_point_in_time(hass, update_cost_and_schedule, next)

    @property
    def native_value(self) -> StateType:
        return self._state

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_state()) is not None:
            self._state = last_sensor_data.state
            self.async_write_ha_state()

    @property
    def should_poll(self):
        return False

    def update_price(self):
        self._state = float(self._state) + self._coste_dia
        self.async_write_ha_state()


class DummySensor(SensorEntity):

    def __init__(self, description: SensorEntityDescription) -> None:
        super().__init__()
        self._state = 0
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = description.key
        self.entity_description = description

    @property
    def native_value(self) -> StateType:
        return self._state

    async def async_added_to_hass(self) -> None:
        self.async_write_ha_state()
