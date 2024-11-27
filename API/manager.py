from storage.duck_db_class import DuckDB
from primewire_class import Primewire
from tqdm import tqdm

class MediaManager(object):
    """docstring for MediaManager"""
    def __init__(self):
        super(MediaManager, self).__init__()
        self.prime = Primewire()
        self.db = DuckDB()
        self.db.set_new_connection("media")
        self.ready_parameters = self.db.get_all_parameters()
        self.ready_parameters = self.ready_parameters.fetchall()

    def get_medias(self) -> None:
        return self.db.get_medias()

    def get_medias_by_category(self, category: str, page: int = int()) -> list[dict]:
        return self.db.get_medias_by_category(category, page)

    def get_medias_by_search(self, search: str, page: int = int()) -> list[dict]:
        return self.db.get_medias_by_search(search, page)

    def get_all_genres(self) -> list[dict]:
        return self.db.get_all_genres()

    def run(self) -> None:
        self.prime.get_filters()
        for genre in tqdm(self.prime.filters):
            page = 1
            while True:
                self.prime.medias = list()
                self.prime.get_media_by_category_page(genre, page)
                if len(self.prime.medias) == 0 or page == 500 or genre == "Action":
                    break
                new_occurrences = [element for element in self.prime.medias 
                                   if element.get("key") not in self.ready_parameters]
                if len(new_occurrences) > 0:
                    self.db.insert_medias(new_occurrences)
                    for term in new_occurrences:
                        self.ready_parameters.append(term["key"])
                print(f"Category: {genre} | Page {page} | New occurrences {len(new_occurrences)}")
                page += 1
