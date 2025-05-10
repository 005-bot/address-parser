import logging
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from importlib.resources import files

import aiosqlite

logger = logging.getLogger(__name__)


@dataclass
class Match:
    name: str
    normalized_name: str
    confidence: float


class AddressParser:
    def __init__(self, db_path: str | None = None):
        """
        Initialize the AddressParser

        :param db_path: path to the SQLite database with streets data
        """
        self._db_path = db_path or str(
            files("address_parser.data").joinpath("streets.db")
        )
        self.db: aiosqlite.Connection | None = None

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self._db_path)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.db:
            await self.db.close()

    async def normalize(self, raw_input: str) -> Match | None:
        """
        Try to normalize the input by removing street types and punctuation.
        If there's a close enough match in the streets database, return it.
        Otherwise, return None.

        :param raw_input: The input to be normalized
        :return: a Match object if the input can be normalized, otherwise None
        """

        candidate = self._clean_name(raw_input)

        return await self._fuzzy_db_match(candidate)

    def _clean_name(self, name: str) -> str:
        name = name.lower().strip()
        # Remove extra spaces and punctuation
        name = re.sub(r"[^\w\s\-]", "", name).strip()
        # Remove extra spaces
        return re.sub(r"\s+", " ", name).strip()

    async def _fuzzy_db_match(self, name: str) -> Match | None:
        if not self.db:
            raise RuntimeError(
                "Database connection not initialized. Use AddressParser within an async context manager."
            )

        candidate: Match | None = None
        s = SequenceMatcher()
        s.set_seq2(name)

        query = """
                SELECT name_normalized, name_original
                FROM streets
                """
        async with self.db.execute(query) as cursor:
            async for result in cursor:
                norm_name, orig_name = result
                if norm_name == name:
                    return Match(
                        name=orig_name, normalized_name=norm_name, confidence=1.0
                    )

                s.set_seq1(norm_name)
                ratio = s.ratio()
                match = s.find_longest_match()

                lcs_score = match.size / max(len(name), 1)
                ratio = ratio * 0.3 + lcs_score * 0.7

                if ratio > 0.6:
                    logger.debug("Found match for %s: %s (%f)", name, orig_name, ratio)

                if candidate is None or ratio > candidate.confidence:
                    candidate = Match(
                        name=orig_name,
                        normalized_name=norm_name,
                        confidence=ratio,
                    )

        return candidate
