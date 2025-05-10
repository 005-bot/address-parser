import argparse
import datetime
import logging
import re
import sqlite3

import overpass
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()


def adapt_datetime_epoch(val):
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())


sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)


def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())


def convert_timestamp(val):
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.datetime.fromtimestamp(int(val))


sqlite3.register_converter("date", convert_date)
sqlite3.register_converter("timestamp", convert_timestamp)


class StreetDBPopulator:
    def __init__(self, db_path: str, region: str = "Красноярск"):
        self.db = sqlite3.connect(db_path)
        self.api = overpass.API(timeout=600)
        self.region = region
        self._init_db()

    def _init_db(self):
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS streets (
                osm_id INTEGER PRIMARY KEY,
                name_normalized TEXT NOT NULL,
                name_original TEXT NOT NULL,
                region TEXT NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        self.db.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS unq_name ON streets(name_normalized)"
        )
        self.db.commit()

    def _normalize_name(self, name: str) -> str:
        name = name.lower().strip()
        # Remove extra spaces and punctuation
        name = re.sub(r"[^\w\s-]", "", name).strip()
        # Remove extra spaces
        return re.sub(r"\s+", " ", name).strip()

    def _get_osm_data(self) -> dict[int, dict]:
        query = f"""
            area[name="{self.region}"]->.searchArea;
            way(area.searchArea)["highway"]["name"];
            out tags;
            """
        try:
            response = self.api.get(query, responseformat="json")
            if not isinstance(response, dict):
                logger.error("Unexpected response type: %s", type(response))
                return {}

            elements = response.get("elements", [])
            if not isinstance(elements, list):
                logger.error("Unexpected 'elements' type: %s", type(elements))
                return {}

            return {
                item["id"]: item["tags"]
                for item in elements
                if isinstance(item, dict) and "id" in item and "tags" in item
            }
        except requests.exceptions.RequestException as e:
            logger.error("OSM API error: %s", e)
            return {}

    def update_streets(self, dry_run: bool = False):
        osm_data = self._get_osm_data()
        if not osm_data:
            return

        for osm_id, tags in osm_data.items():
            if "name" not in tags:
                continue

            original_name = tags["name"]
            normalized = self._normalize_name(original_name)
            if "площадь" in normalized:
                continue

            self.db.execute(
                """INSERT OR REPLACE INTO streets 
                (osm_id, name_normalized, name_original, region, last_updated)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    osm_id,
                    normalized,
                    original_name,
                    self.region,
                    datetime.datetime.now(),
                ),
            )

        if not dry_run:
            self.db.commit()
            logger.info("Updated %d streets", len(osm_data))
        else:
            self.db.rollback()
            logger.info("Dry run: Would update %d streets", len(osm_data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default="Красноярск", help="Target region name")
    parser.add_argument("--dry-run", action="store_true", help="Test without saving")
    parser.add_argument(
        "--db-path",
        default="src/address_parser/data/streets.db",
        help="Database file path",
    )
    args = parser.parse_args()

    populator = StreetDBPopulator(args.db_path, args.region)
    populator.update_streets(args.dry_run)
