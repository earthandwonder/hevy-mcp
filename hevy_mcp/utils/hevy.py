"""Hevy API client."""

import httpx

from hevy_mcp.utils.auth import get_credentials

BASE_URL = "https://api.hevyapp.com/v1"


class HevyClient:
    """Async Hevy API client with static API key auth."""

    def _headers(self) -> dict[str, str]:
        creds = get_credentials()
        return {
            "api-key": creds["api_key"],
            "Accept": "application/json",
        }

    async def get(self, path: str, params: dict | None = None) -> dict:
        """GET request to the Hevy API. Returns JSON response."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BASE_URL}{path}",
                headers=self._headers(),
                params=params,
            )
            resp.raise_for_status()
        return resp.json()

    async def post(self, path: str, json: dict | None = None) -> dict:
        """POST request to the Hevy API. Returns JSON response."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}{path}",
                headers={**self._headers(), "Content-Type": "application/json"},
                json=json,
            )
            if not resp.is_success:
                detail = resp.text
                raise httpx.HTTPStatusError(
                    f"HTTP {resp.status_code} for {resp.url}: {detail}",
                    request=resp.request,
                    response=resp,
                )
        return resp.json()

    async def put(self, path: str, json: dict | None = None) -> dict:
        """PUT request to the Hevy API. Returns JSON response."""
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"{BASE_URL}{path}",
                headers={**self._headers(), "Content-Type": "application/json"},
                json=json,
            )
            if not resp.is_success:
                detail = resp.text
                raise httpx.HTTPStatusError(
                    f"HTTP {resp.status_code} for {resp.url}: {detail}",
                    request=resp.request,
                    response=resp,
                )
        return resp.json()

    async def get_paginated(self, path: str, params: dict | None = None) -> list[dict]:
        """GET all pages from a paginated Hevy endpoint. Returns combined results."""
        params = dict(params or {})
        params.setdefault("page", 1)
        params.setdefault("pageSize", 10)

        all_items = []
        while True:
            data = await self.get(path, params=params)
            # Hevy wraps paginated data in a key that varies by endpoint
            # The common patterns are: workouts, routines, exercise_templates
            for key in ("workouts", "routines", "exercise_templates"):
                if key in data:
                    all_items.extend(data[key])
                    break

            page = data.get("page", 1)
            page_count = data.get("page_count", 1)
            if page >= page_count:
                break
            params["page"] = page + 1

        return all_items


hevy_client = HevyClient()
