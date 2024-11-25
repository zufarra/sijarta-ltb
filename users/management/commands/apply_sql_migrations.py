import os

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Apply raw SQL migrations from the migrations folder."

    def handle(self, *args, **kwargs):
        migrations_dir = os.path.join(os.path.dirname(__file__), "../../../migrations")
        applied_migrations = self.get_applied_migrations()

        for file in sorted(os.listdir(migrations_dir)):
            if file.endswith(".sql") and file not in applied_migrations:
                file_path = os.path.join(migrations_dir, file)
                self.apply_migration(file_path, file)

    def get_applied_migrations(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS migration_history (
                    id SERIAL PRIMARY KEY,
                    migration_name VARCHAR(255) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            cursor.execute("SELECT migration_name FROM migration_history")
            return {row[0] for row in cursor.fetchall()}

    def apply_migration(self, file_path, file_name):
        with open(file_path, "r", encoding="utf-8") as f:
            sql = f.read()
        try:
            with connection.cursor() as cursor:
                cursor.execute("BEGIN;")
                cursor.execute(sql)
                cursor.execute(
                    "INSERT INTO migration_history (migration_name) VALUES (%s)",
                    [file_name],
                )
                cursor.execute("COMMIT;")
                self.stdout.write(self.style.SUCCESS(f"Applied migration: {file_name}"))
        except Exception as e:
            with connection.cursor() as cursor:
                cursor.execute("ROLLBACK;")
            self.stderr.write(self.style.ERROR(f"Failed migration {file_name}: {e}"))
