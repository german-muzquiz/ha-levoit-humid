"""
Custom integration to integrate vesync_humidifiers with Home Assistant.

For more details about this integration, please refer to
https://github.com/german-muzquiz/ha-vesync-humidifier
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.loader import async_get_loaded_integration

from .api import VesyncApiClient
from .const import DOMAIN, LOGGER
from .coordinator import VesyncDataUpdateCoordinator
from .data import VesyncData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import VesyncConfigEntry

PLATFORMS: list[Platform] = [
    Platform.HUMIDIFIER,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: VesyncConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = VesyncDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(seconds=30),
    )
    entry.runtime_data = VesyncData(
        client=VesyncApiClient(
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: VesyncConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: VesyncConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
