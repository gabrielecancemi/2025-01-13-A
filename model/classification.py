from dataclasses import dataclass


@dataclass
class Classification:
    GeneID: str
    Localization: str
    Essential: str

    def __hash__(self):
        return hash(self.GeneID)

    def __eq__(self, other):
        return self.GeneID == other.GeneID

    def __str__(self):
        return self.GeneID