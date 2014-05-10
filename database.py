import sqlite3
import os
import errno

IMG_TYPES = ['jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff']
DATA_DIR = os.path.join(os.path.expanduser('~'), 'webcrawled', 'images')
DATABASE_FILE = \
    os.path.join(os.path.expanduser('~'), 'webcrawled', 'crawled.db')

class ImageDatabase:

    def __init__(self, filepath):
        self.db_file = filepath
        if not os.path.exists(self.db_file):
            try:
                os.makedirs('/'.join(filepath.split('/')[0:-1]))
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
            self.conn = sqlite3.connect(self.db_file)
            self.initialize_tables()
        else:
            self.conn = sqlite3.connect(self.db_file)

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
                total_bytes INTEGER,
                num_images INTEGER,
                pages_crawled INTEGER
            );
            """)
        self.conn.execute("""
                INSERT INTO stat VALUES ('%s', 0, 0, 0)
                ;
            """ % DATA_DIR)
        self.conn.commit()

    def create_image_entry(self, url, name, sess_time, byte_size):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM images WHERE name = '%s'
            """ % name)
        if cur.fetchone() is None:
            self.conn.execute("""
                INSERT INTO images VALUES (?, ?, ?, ?, NULL)
                ;
                """, (url, name, sess_time, byte_size))
            self.conn.execute("""
                UPDATE stat SET
                    total_bytes = (SELECT total_bytes FROM stat) + %s,
                    num_images = (SELECT num_images FROM stat) + 1
                    ;
                """ % byte_size)
            self.conn.commit()
        else:
            pass # TODO: update a table of possible false positive duplicates

    def inc_pages_crawled(self):
        self.conn.execute("""
            UPDATE stat SET
                pages_crawled = (SELECT pages_crawled FROM stat) + 1
                ;
            """)
        self.conn.commit()

    def read_image_entry(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM images;
        """)
        print cur.fetchall()

    def update_image(self):
        pass

    def delete_image(self):
        pass
