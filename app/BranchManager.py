# BranchManager.py
import logging
from logger_config import setup_logger

logger = setup_logger()

class BranchManager:
    """Управляет данными филиалов."""

    def __init__(self, branch_mapping):
        self.branch_mapping = branch_mapping
        logger.info("BranchManager initialized")

    def get_branch_email(self, city):
        """Возвращает email филиала для указанного города."""
        logger.info(f"Retrieving email for city {city}")
        email = self.branch_mapping.get(city.lower())
        logger.info(f"Retrieved email {email} for city {city}")
        return email