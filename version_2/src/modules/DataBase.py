from typing import List, Optional, Tuple, Any
import sqlite3
import os

class DataBase:
    """
    @class DataBase
    @brief Manages SQLite database operations for storing component information.
    
    Handles database initialization, insertion, querying, and deletion of component records.
    """
    def __init__(self, logger, filemanager): 
        """
        @brief Constructs the database manager.
        @param logger Logger instance for logging events and errors.
        @param filemanager FileManager instance for handling filesystem operations.
        """

        self._log = logger
        self._file = filemanager

        self._path = "Data"
        self._db_path =  "/home/ruimc/Projetos/PythonProjects/echoGabinnet/Data/database.db"
        self._table = "components"

        self.__initialize()


    def __connect(self) -> sqlite3.Connection:
        """
        @brief Establishes and returns a connection to the SQLite database.
        @return sqlite3.Connection object
        @throws sqlite3.OperationalError on connection failure
        """
        try:
            return sqlite3.connect(self._db_path)
        except sqlite3.OperationalError as e:
            self._log.write_log("Logs/databaseOperations.log", "ERROR", f"Database connection failed: {e}")
            raise


    def __initialize(self) -> None:
        """
        @brief Ensures the database directory, file, and schema are properly initialized.
        """
        self._file.create_dir(self._path)
        self._create_db_file()
        self._create_table()


    def _create_db_file(self) -> None:
        """
        @brief Creates the database file if it doesn't exist.
        """
        if not self._file.file_exists(self._db_path):
            self._file.create_file(self._db_path)
            self._log.write_log("Logs/databaseOperations.log", "INFO", "Database file created.")


    def _create_table(self) -> None:
        """
        @brief Creates the components table if it doesn't exist.
        """
        query = f"""
            CREATE TABLE IF NOT EXISTS {self._table}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                componentName TEXT NOT NULL,
                position INTEGER NOT NULL,
                description TEXT NOT NULL
            );
        """
        try:
            with self.__connect() as conn:
                #cursor = conn.cursor()
                conn.execute(query)
                conn.commit()
                self._log.write_log("Logs/databaseOperations.log", "INFO", "Table initialized successfully.")
        except Exception as e:
            self._log.write_log("Logs/databaseOperations.log", "ERROR", f"Failed to create table: {e}")



    def insert_component(self, name: str, position: int, description: str) -> None:
        """
        @brief Inserts a new component into the database.
        @param name Name of the component.
        @param position Position value.
        @param description Description of the component.
        """

        query = f"INSERT INTO {self._table} (componentName, position, description) VALUES (?, ?, ?)"
        try:
            with self.__connect() as conn:
                #cursor = conn.cursor()
                conn.execute(query, (name, position, description))
                conn.commit()
        except Exception as e:
            self._log.write_log("Logs/databaseOperations.log", "ERROR", f"Failed to insert component: {e}")



    def delete_component(self, name: str) -> None:
        """
        @brief Deletes a component by name.
        @param name Name of the component to delete.
        """
        query = f"DELETE FROM {self._table} WHERE componentName = ?"
        try:
            with self.__connect() as conn:
                conn.execute(query, (name,))
                conn.commit()

        except Exception as e:
            self._log.write_log("Logs/databaseOperations.log", "ERROR", f"Failed to delete component: {e}")
    


    def search_component(self, name: str) -> List[Tuple[Any]]:
        """
        @brief Searches for a component by name.
        @param name Name of the component.
        @return List of matching records as tuples.
        """
        query = f"SELECT * FROM {self._table} WHERE componentName = ?"
        try:
            with self._connect() as conn:
                cursor = conn.execute(query, (name,))
                return cursor.fetchall()
        except Exception as e:
            self._log.write_log("Logs/databaseOperations.log", "ERROR", f"Search failed for {name}: {e}")
            return []
        

    def get_position(self, name: str) -> Optional[int]:
        """
        @brief Gets the position of a component by name.
        @param name Name of the component.
        @return Position as integer, or None if not found.
        """

        query = f"SELECT position FROM {self._table} WHERE componentName = ?;"

        try:
            with self._connect() as conn:
                cursor = conn.execute(query, (name,))
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            self._log.write_log("Logs/databaseOperations.log", "ERROR", f"Get position failed for {name}: {e}")
            return None


    def get_all_components(self) -> List[Tuple[str, int, str]]:
        """
        @brief Retrieves all components from the database.
        @return List of tuples containing (componentName, position, description).
        """
        query = f"SELECT * FROM {self._table}"
        try:
            with self._connect() as conn:
                cursor = conn.execute(query)
                result = cursor.fetchall()
                return [(row[1], row[2], row[3]) for row in result]
        except Exception as e:
            self._log.write_log("Logs/databaseOperations.log", "ERROR", f"Fetch all components failed: {e}")
            return []
    
