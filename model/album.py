from dataclasses import dataclass


@dataclass
class Album:
    AlbumId: int
    Title: str
    durata: float      # in minuti

    def __hash__(self):
        return hash(self.AlbumId)

    def __eq__(self, other):
        return isinstance(other, Album) and self.AlbumId == other.AlbumId

    def __str__(self):
        return self.Title