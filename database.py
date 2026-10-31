import sqlite3

class DatabaseManager:
    """Класс для управления рекордами и статистикой в SQLite."""
    def __init__(self, db_name="geometry_records.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Создает таблицы и инициализирует 4 уровня."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS levels (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                max_x INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                level_id INTEGER PRIMARY KEY,
                best_progress INTEGER DEFAULT 0,
                attempts INTEGER DEFAULT 0,
                FOREIGN KEY (level_id) REFERENCES levels(id)
            )
        ''')
        # Добавляем все 4 уровня в базу
        levels_data = [
            (1, "Stereo Madness Clone", 2200),
            (2, "Back On Track Clone", 2200),
            (3, "Polargeist Clone", 2200),
            (4, "Dry Out Clone", 2200)  # НОВЫЙ 4-й уровень
        ]
        for lvl_id, name, max_x in levels_data:
            cursor.execute("INSERT OR IGNORE INTO levels (id, name, max_x) VALUES (?, ?, ?)", (lvl_id, name, max_x))
            cursor.execute("INSERT OR IGNORE INTO records (level_id) VALUES (?)", (lvl_id,))
        conn.commit()
        conn.close()

    def increment_attempt(self, level_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE records SET attempts = attempts + 1 WHERE level_id = ?", (level_id,))
        conn.commit()
        conn.close()

    def save_record(self, level_id, progress_percent):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT best_progress FROM records WHERE level_id = ?", (level_id,))
        row = cursor.fetchone()
        if row and progress_percent > row[0]:
            cursor.execute("UPDATE records SET best_progress = ? WHERE level_id = ?", (progress_percent, level_id))
            print(f"Новый рекорд для Уровня {level_id}: {progress_percent}%!")
        conn.commit()
        conn.close()

    def get_stats(self, level_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT attempts, best_progress FROM records WHERE level_id = ?", (level_id,))
        row = cursor.fetchone()
        conn.close()
        return row if row else (0, 0)