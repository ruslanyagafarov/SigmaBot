class BranchManager:
    """Управляет данными филиалов."""

    def __init__(self, branch_mapping):
        self.branch_mapping = branch_mapping

    def get_branch_email(self, city):
        """Возвращает email филиала для указанного города."""
        return self.branch_mapping.get(city.lower())
