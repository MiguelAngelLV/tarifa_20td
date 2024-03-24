"""Create and add sensors to Home Assistant."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Mapping

import pytz
from tariff_td import Tariff20TD, Tariff30TD, TariffTD
from typing_extensions import override

from homeassistant.components.sensor import (
    RestoreEntity,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.helpers.event import async_track_point_in_time

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
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

TIMEZONE = pytz.timezone("Europe/Madrid")

TARIFF_TD_DESCRIPTION = SensorEntityDescription(
    key="precio_20td",
    icon="mdi:currency-eur",
    name="Precio kWh",
    device_class=SensorDeviceClass.MONETARY,
    native_unit_of_measurement="€/kWh",
)

FIXED_DESCRIPTION = SensorEntityDescription(
    key="coste_fijo_20td",
    icon="mdi:currency-eur",
    name="Costes Fijos Totales",
    state_class=SensorStateClass.TOTAL_INCREASING,
    native_unit_of_measurement="€",
)

DUMMY_DESCRIPTION = SensorEntityDescription(
    key="coste_fijo_kwh",
    icon="mdi:currency-eur",
    name="Costes Fijos",
    device_class=SensorDeviceClass.ENERGY,
    state_class=SensorStateClass.TOTAL_INCREASING,
    native_unit_of_measurement="kWh",
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Configure and add sensors to Home Assistant."""
    p1 = float(entry.data.get(CONF_P1, 0))
    p2 = float(entry.data.get(CONF_P2, 0))
    p3 = float(entry.data.get(CONF_P3, 0))
    p4 = float(entry.data.get(CONF_P4, 0))
    p5 = float(entry.data.get(CONF_P5, 0))
    p6 = float(entry.data.get(CONF_P6, 0))
    tariff = entry.data[CONF_TARIFF]
    diary = float(entry.data.get(CONF_DIARY_COST, 0))

    tariff_td = (
        Tariff20TD(p1, p2, p3)
        if tariff == TARIFF_20
        else Tariff30TD(p1, p2, p3, p4, p5, p6)
    )

    dummy_sensor = DummySensor(DUMMY_DESCRIPTION, entry.entry_id)
    fixed_sensor = FixedSensor(FIXED_DESCRIPTION, diary, hass, entry.entry_id)
    tariff_sensor = TariffTDSensor(
        TARIFF_TD_DESCRIPTION, tariff_td, hass, entry.entry_id
    )
    async_add_entities([fixed_sensor, dummy_sensor, tariff_sensor])


class TariffTDSensor(SensorEntity):
    """Create a sensor with actual price per kWh and period from spanish Tariff TD."""

    def __init__(
        self,
        description: SensorEntityDescription,
        tariff: TariffTD,
        hass: HomeAssistant,
        unique: str,
    ) -> None:
        """Initialise values."""
        super().__init__()
        self._state = None
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = f"{unique}-{description.key}"
        self.entity_description = description
        self._tariff = tariff

        async def update_price_and_schedule(time: datetime) -> None:
            self.update_price()
            next_update = time + timedelta(hours=1)
            async_track_point_in_time(hass, update_price_and_schedule, next_update)

        now = datetime.now(tz=TIMEZONE)
        first_update = now.replace(minute=0, second=0) + timedelta(hours=1)
        async_track_point_in_time(hass, update_price_and_schedule, first_update)

    @property
    @override
    def native_value(self) -> StateType:
        return self._state

    @property
    @override
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return {"Period": self._tariff.get_period(datetime.now(tz=TIMEZONE))}

    @override
    async def async_added_to_hass(self) -> None:
        self.update_price()

    @property
    @override
    def should_poll(self) -> bool:
        return False

    def update_price(self) -> None:
        """Update the price each hour."""
        self._state = self._tariff.get_price(datetime.now(tz=TIMEZONE))
        self.async_write_ha_state()


class FixedSensor(SensorEntity, RestoreEntity):
    """Calculate the fixed cost per day and generate a sensor with total cost."""

    def __init__(
        self,
        description: SensorEntityDescription,
        cost_per_day: float,
        hass: HomeAssistant,
        unique: str,
    ) -> None:
        """Initialise values."""
        super().__init__()
        self._state = 0
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = f"{unique}-{description.key}"
        self.entity_description = description
        self._cost_per_day = cost_per_day

        async def update_cost_and_schedule(time: datetime) -> None:
            self.update_price()
            next_update = time + timedelta(days=1)
            async_track_point_in_time(hass, update_cost_and_schedule, next_update)

        now = datetime.now(tz=TIMEZONE)
        first_update = now.replace(hour=0, minute=5, second=0) + timedelta(days=1)
        async_track_point_in_time(hass, update_cost_and_schedule, first_update)

    @property
    @override
    def native_value(self) -> StateType:
        return self._state

    @override
    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_state()) is not None:
            self._state = last_sensor_data.state
            self.async_write_ha_state()

    @property
    @override
    def should_poll(self) -> bool:
        return False

    def update_price(self) -> None:
        """Increase the total price each day."""
        self._state = float(self._state) + self._cost_per_day
        self.async_write_ha_state()


class DummySensor(SensorEntity):
    """Dummy Sensor for use in Energy Dashboard for calculate fixed cost."""

    def __init__(self, description: SensorEntityDescription, unique: str) -> None:
        """Initialise values."""
        super().__init__()
        self._state = 0
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = f"{unique}-{description.key}"
        self.entity_description = description

    @property
    @override
    def native_value(self) -> StateType:
        return self._state

    @override
    async def async_added_to_hass(self) -> None:
        self.async_write_ha_state()
