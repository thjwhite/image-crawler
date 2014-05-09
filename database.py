import sqlite3
import os

class ImageDatabase:

    def __init__(self, filepath):
        self.db_file = filepath
        self.conn = sqlite3.connect(self.db_file)
        if not os.path.exists(self.db_file):
            self.initialize_tables()

    def initialize_tables(self):
        self.conn.execute("""
            CREATE TABLE images
            (
                url TEXT,
                name TEXT UNIQUE,
                page_session_time INTEGER,
                byte_size INTEGER,
                id INTEGER PRIMARY KEY
            );
            """)
        self.conn.execute("""
            CREATE TABLE stat
            (
                data_dir TEXT,
                total_byte INTEGER,
                num_images INTEGER,
                pages_crawled INTEGER
            );
            """)
        self.conn.commit()

    def create_image_entry(self, url, name, sess_time, byte_size):
        self.conn.execute("""
            INSERT INTO images VALUES (?, ?, ?, ?, NULL);
        """, (url, name, sess_time, bytes_size))

    def read_image_entry(self):
        cur = self.conn.cursor()


    def update_image(self):
        pass

    def delete_image(self):
        pass
