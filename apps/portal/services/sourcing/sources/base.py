"""
Base Scraper Interface for DBERT LMS Sourcing Engine
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScraper(ABC):
    name: str = "base"
    region: str = "International"

    @abstractmethod
    def fetch_leads(self, target_count: int = 500) -> List[Dict[str, Any]]:
        """
        Fetches job / internship leads.
        Returns a list of dicts with keys:
          - Domain
          - Company
          - Role
          - Location
          - Is_Remote
          - Start_Date
          - End_Date
          - Stipend
          - URL
          - Description
          - Source
          - Region
        """
        pass
