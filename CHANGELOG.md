# Changelog

## 3 March 2026

### Permission Fixes
- Fixed `sqlite3.OperationalError: attempt to write a readonly database` by adjusting file and directory permissions for the SQLite database.
  - Ran `chmod 664 database.db` on project root database file.
  - Ran `chmod 775 .` on project root directory to allow directory write access.
  - Verified write access with a manual `INSERT` using the `sqlite3` CLI.
  - Provided explanation of how to reset ownership if necessary (`sudo chown $USER database.db`).
  - Suggested a development "nuclear" fix: deleting the database file and allowing the app to recreate it.

### Pydantic Warning
- Noted and advised update for Pydantic v2:
  - Replace `class Config: orm_mode = True` with `model_config = { "from_attributes": True }`.

### Additional Notes
- Documented that SELECT queries were working while INSERTs were failing due to permissions, confirming the root cause.
- Included follow-up steps for restarting the FastAPI server and retesting endpoints.

*File created to track project changes and fixes.*
