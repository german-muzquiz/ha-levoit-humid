"""DataUpdateCoordinator for vesync_humidifiers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    VesyncApiAuthenticationError,
    VesyncApiClientError,
)

if TYPE_CHECKING:
    from .data import VesyncConfigEntry
from .const import LOGGER


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class VesyncDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: VesyncConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            LOGGER.info("Updating data")
            return await self.config_entry.runtime_data.client.async_get_data()
        except VesyncApiAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except VesyncApiClientError as exception:
            raise UpdateFailed(exception) from exception
