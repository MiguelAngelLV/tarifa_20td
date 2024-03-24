from typing import Mapping, Any
from datetime import datetime, timedelta
from tariff_td import TariffTD, Tariff30TD, Tariff20TD
from .const import (
    CONF_P1,
    CONF_P2,
    CONF_P3,
    CONF_P4,
    CONF_P5,
    CONF_P6,
    CONF_DIARY_COST,
    CONF_TARIFF,
    TARIFF_20
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
    RestoreEntity
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.event import async_track_point_in_time

TARIFF_TD_DESCRIPTION = SensorEntityDescription(
    key="precio_20td",
    icon="mdi:currency-eur",
    name="Precio kWh",
    device_class=SensorDeviceClass.MONETARY,
    native_unit_of_measurement="€/kWh"
)

FIXED_DESCRIPTION = SensorEntityDescription(
    key="coste_fijo_20td",
    icon="mdi:currency-eur",
    name="Costes Fijos Totales",
    state_class=SensorStateClass.TOTAL_INCREASING,
    native_unit_of_measurement="€"
)

DUMMY_DESCRIPTION = SensorEntityDescription(
    key="coste_fijo_kwh",
    icon="mdi:currency-eur",
    name="Costes Fijos",
    device_class=SensorDeviceClass.ENERGY,
    state_class=SensorStateClass.TOTAL_INCREASING,
    native_unit_of_measurement="kWh"
)


async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    p1 = float(entry.data.get(CONF_P1, 0))
    p2 = float(entry.data.get(CONF_P2, 0))
    p3 = float(entry.data.get(CONF_P3, 0))
    p4 = float(entry.data.get(CONF_P4, 0))
    p5 = float(entry.data.get(CONF_P5, 0))
    p6 = float(entry.data.get(CONF_P6, 0))
    tariff = entry.data[CONF_TARIFF]
    diary = float(entry.data.get(CONF_DIARY_COST, 0))

    tariff_td = Tariff20TD(p1, p2, p3) if tariff == TARIFF_20 else Tariff30TD(p1, p2, p3, p4, p5, p6)

    dummy_sensor = DummySensor(DUMMY_DESCRIPTION, entry.entry_id)
    fixed_sensor = FixedSensor(FIXED_DESCRIPTION, diary, hass, entry.entry_id)
    tariff_sensor = TariffTDSensor(TARIFF_TD_DESCRIPTION, tariff_td, hass, entry.entry_id)
    async_add_entities([fixed_sensor, dummy_sensor, tariff_sensor])


class TariffTDSensor(SensorEntity):

    def __init__(self, description: SensorEntityDescription, tariff: TariffTD, hass, unique: str) -> None:
        super().__init__()
        self._state = None
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = f"{unique}-{description.key}"
        self.entity_description = description
        self._tariff = tariff

        async def update_price_and_schedule(time):
            self.update_price()
            next_update = time + timedelta(hours=1)
            async_track_point_in_time(hass, update_price_and_schedule, next_update)

        now = datetime.now()
        next = now.replace(minute=0, second=0) + timedelta(hours=1)
        async_track_point_in_time(hass, update_price_and_schedule, next)

    @property
    def native_value(self) -> StateType:
        return self._state

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return {'Period': self._tariff.get_period()}

    async def async_added_to_hass(self) -> None:
        self.update_price()

    @property
    def should_poll(self):
        return False

    def update_price(self):
        self._state = self._tariff.get_price()
        self.async_write_ha_state()


class FixedSensor(SensorEntity, RestoreEntity):

    def __init__(self, description: SensorEntityDescription, cost_per_day, hass, unique: str) -> None:
        super().__init__()
        self._state = 0
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = f"{unique}-{description.key}"
        self.entity_description = description
        self._cost_per_day = cost_per_day

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
        self._state = float(self._state) + self._cost_per_day
        self.async_write_ha_state()


class DummySensor(SensorEntity):

    def __init__(self, description: SensorEntityDescription, unique) -> None:
        super().__init__()
        self._state = 0
        self._attrs: Mapping[str, Any] = {}
        self._attr_name = description.name
        self._attr_unique_id = f"{unique}-{description.key}"
        self.entity_description = description

    @property
    def native_value(self) -> StateType:
        return self._state

    async def async_added_to_hass(self) -> None:
        self.async_write_ha_state()
