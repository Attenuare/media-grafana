from io import TextIOWrapper
from zipfile import ZipFile
from typing import Union
from pathlib import Path
from tqdm import tqdm
import duckdb
import os


class DuckDB(object):
    """
        Class used to manipulate files and
        also connect to a duck databse instance
    """
    def __init__(self):
        self.my_path = os.getcwd().replace('\\', '/')
        self.results = list()
        self.connection, self.reader, self.metadata = None, None, None
        self.debug = bool()

    def set_new_connection(self, database: str="generic", threads: int=1, metadata: bool=bool()) -> None:
        dbs_path = Path(f"{self.my_path}/databases")
        if not dbs_path.is_dir():
            dbs_path.mkdir()
        if not metadata:
            self.connection = duckdb.connect(f"{self.my_path}/databases/{database}.db", config={'threads': threads})
        else:
            self.metadata = duckdb.connect(f"{self.my_path}/databases/{database}.db", config={'threads': threads})

    def db_sql(self, query: str, metadata: bool=bool()) -> None:
        if self.debug:
            print(query)
        if metadata:
            self.results_metadata = self.metadata.sql(query)
            return
        if self.connection:
            self.results = self.connection.sql(query)

    def close_connection(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None

    def read_ziped_csv(self, file_name: str) -> None:  # type: ignore
        if Path(f"{self.my_path}/data_files/ziped_files/{file_name}.zip").is_file():
            zf = ZipFile(f"{self.my_path}/data_files/ziped_files/{file_name}.zip")
            file_path = zf.namelist()[0] if len(zf.namelist()[0]) > 0 else None
            if file_path:
                self.reader = duckdb.read_csv(TextIOWrapper(zf.open(file_path), 'latin-1'), 
                                              delimiter=';', all_varchar=True, header=False, quotechar='"')

    def create_tables(self, entities: dict) -> None:
        [self.db_sql(f"CREATE TABLE {table} ({' VARCHAR, '.join(list(entities[table].keys()))} VARCHAR)") 
        for table in tqdm(list(entities.keys()), desc="Creating tables...")]

    def create_metadata(self, entities: dict) -> None:
        self.set_new_connection("cnpjs_metadata")
        [self.db_sql(f"CREATE SEQUENCE {table}_id_seq; CREATE TABLE {table} (id INTEGER DEFAULT nextval('{table}_id_seq'), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, code VARCHAR, count INTEGER)") 
        for table in tqdm(list(entities.keys()), desc="Creating tables...")]

    def create_meta_index(self, entities: dict) -> None:
        self.set_new_connection("cnpjs_metadata")
        [self.db_sql(f"CREATE SEQUENCE {table}_id_seq_index; CREATE TABLE {table}_meta (id INTEGER DEFAULT nextval('{table}_id_seq'), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, cnpj_basico VARCHAR, group_ VARCHAR, from_ INTEGER)") 
        for table in tqdm(list(entities.keys()), desc="Creating tables...")]

    def create_media_table(self) -> None:
        print("Creating table media")
        sql_query = """
                    CREATE SEQUENCE media_id_seq_index;
                    CREATE TABLE media (
                        id INTEGER DEFAULT nextval('media_id_seq_index') PRIMARY KEY,
                        key TEXT,
                        link TEXT,
                        image TEXT,
                        title TEXT,
                        categories TEXT,
                        rating INTEGER,
                        year INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """
        self.db_sql(sql_query)

    def get_all_parameters(self) -> None:
        sql_query = """SELECT key FROM media"""
        self.db_sql(sql_query)
        return self.results

    def insert_medias(self, medias: list) -> None:
        keys = ["key", "link", "image", "title", "categories", "rating", "year"]
        values = list()
        for element in medias:
            value = [f"'{element[key]}'" if type(element[key]) is str else str(element[key]) for key in keys]
            value = f"({','.join(value)})"
            values.append(value)
        sql_query = f"""INSERT INTO media (key, link, image, title, categories, rating, year) VALUES {','.join(values)}"""
        self.db_sql(sql_query)

    def get_medias(self, page: int) -> None:
        sql_query = 'SELECT key, link, image, title, categories, rating, year FROM media'
        return self.__manage_pagination(sql_query, page, 
                                        ["key", "link", "image", "title", "categories", "rating", "year"])

    def __manage_pagination(self, query: str, page: int, keys: list) -> list[dict]:
        offset = 100 * page
        limit = offset + 100
        sql_query = query + f''' OFFSET {offset} LIMIT {limit}'''
        self.db_sql(sql_query)
        return [dict(zip(keys, result)) for result in self.results.fetchall()]

    def get_medias_by_category(self, category: str, page: Union[int, None] = None) -> None:
        sql_query = f'''
            SELECT key, link, image, title, categories, rating, year 
            FROM media WHERE categories LIKE '%{category}%' 
        '''
        return self.__manage_pagination(sql_query, page, 
                                        ["key", "link", "image", "title", "categories", "rating", "year"])

    def get_medias_by_search(self, search: str, page: Union[int, None] = None) -> None:
        sql_query = f'''
            SELECT key, link, image, title, categories, rating, year 
            FROM media WHERE title LIKE '%{search}%' 
        '''
        return self.__manage_pagination(sql_query, page, 
                                        ["key", "link", "image", "title", "categories", "rating", "year"])

    def get_all_genres(self) -> None:
        sql_query = f'''SELECT DISTINCT trim(UNNEST(string_to_array(categories, ';'))) FROM media'''
        self.db_sql(sql_query)
        return [term[0] for term in self.results.fetchall() if len(term) > 0]

    def get_all_genres(self) -> None:
        sql_query = f'''SELECT DISTINCT trim(UNNEST(string_to_array(categories, ';'))) FROM media'''
        self.db_sql(sql_query)
        return [term[0] for term in self.results.fetchall() if len(term) > 0]

    def get_best_recommendations(self, page: Union[int, None] = None) -> None:
        sql_query = f'''SELECT key, link, image, title, categories, rating, year FROM media ORDER BY rating DESC'''
        return self.__manage_pagination(sql_query, page, 
                                        ["key", "link", "image", "title", "categories", "rating", "year"])
    
    def get_best_recommendations_by_year(self, page: Union[int, None] = None) -> None:
        sql_query = '''
                    SELECT m.key, m.link, m.image, m.title, m.categories, m.rating, m.year
                    FROM media m
                    JOIN (
                        SELECT year, MAX(rating) AS max_rating
                        FROM media
                        GROUP BY year
                    ) AS max_ratings
                    ON m.year = max_ratings.year AND m.rating = max_ratings.max_rating
                    ORDER BY m.year DESC    
                    '''
        return self.__manage_pagination(sql_query, page, 
                                        ["key", "link", "image", "title", "categories", "rating", "year"])
    
    def get_best_recommendations_by_year_filter(self, search: int ,page: Union[int, None] = None) -> None:
        sql_query = f'''
                    SELECT m.key, m.link, m.image, m.title, m.categories, m.rating, m.year
                    FROM media m
                    JOIN (
                        SELECT year, MAX(rating) AS max_rating
                        FROM media
                        GROUP BY year
                    ) AS max_ratings
                    ON m.year = max_ratings.year AND m.rating = max_ratings.max_rating
                    AND m.year = {search}
                    ORDER BY m.year DESC    
                    '''
        return self.__manage_pagination(sql_query, page, 
                                        ["key", "link", "image", "title", "categories", "rating", "year"])

