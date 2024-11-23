from request_manager.manager import RequestManager


class Primewire(RequestManager):
    """
        Class used to extract information from
        the website primewire
        
    """
    def __init__(self) -> None:
        super(Primewire, self).__init__()
        self.primordial_link = "https://www.primewire.tf"
        self.filters = list()
        self.medias = list()
    
    def get_filters(self) -> None:
        self.send_requisitons_requests(self.primordial_link)
        if self.availiable:
            filters = self.soup.find("ul", {"class": "menu-genre-list"})
            self.filters = [term.text.strip() for term in filters("li")]

    def __build_media_json(self, occurrence: object) -> bool:
        box_info = occurrence.a
        link = box_info.get("href")
        image = box_info.img.get("src") if box_info.img else None
        categories = occurrence.find("div", {"class": "item_categories"})
        categories = categories("a") if categories else list()
        rating = occurrence.find("li", {"class": "current-rating"})
        rating = rating.attrs.get("style", str()).replace("width: ", str()).replace(";", str()).replace("px", str())
        title = box_info.get("title", str()).strip().replace("'"," ")
        year = title.split(" ")[-1].replace(")", str()).replace("(", str()).strip() if len(title.split(" ")) > 0 else str()
        year = int(year) if year.isdigit() else 0
        try:
            key = int(link.split("/")[-1].split("-")[0])
        except Exception as e:
            return False
        self.media_occurrence = {
            "key": key,
            "link": self.primordial_link + link if link else str(),
            "image": self.primordial_link + image if image else str(),
            "title": title,
            "categories": "; ".join([term.text.strip() for term in categories]),
            "rating": rating,
            "year": year
        }
        if self.media_occurrence not in self.medias:
            self.medias.append(self.media_occurrence)

    def get_media_by_category_page(self, genre: str, page: int) -> None:
        self.send_requisitons_requests(f"https://www.primewire.tf/filter?genre[]={genre}&page={page}")
        media_box = self.soup.find_all("div", {"class": "index_item index_item_ie"})
        self.media_box = media_box
        if len(media_box) > 0:
            for occurrence in media_box:
                self.__build_media_json(occurrence)
