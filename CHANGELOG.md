# Changelog

## 3 March 2026

### Database permission fix

**Resolved error**

`sqlite3.OperationalError: attempt to write a readonly database`

**Root cause**

SQLite database file and/or project directory lacked write permissions, which blocked `INSERT` operations while still allowing `SELECT` queries.

**Resolution**

- Updated database file permissions:
  - `chmod 664 database.db`
- Updated project root directory permissions:
  - `chmod 775 .`
- Verified write access using the `sqlite3` CLI with a manual `INSERT`
- Documented ownership reset option:
  - `sudo chown $USER database.db`
- Added development fallback:
  - `rm database.db` (allow the app to recreate the database)

**Result**

User registration (`POST /auth/register`) now completes successfully without 500 errors.

---

### Pydantic v2 migration

**Addressed deprecation warning**

`'orm_mode' has been renamed to 'from_attributes'`

**Configuration change**

Before (Pydantic v1):

```python
class Config:
    orm_mode = True
```

After (Pydantic v2):

```python
model_config = {
    "from_attributes": True
}
```

---

### Verification

- Restarted FastAPI server
- Retested:
  - `POST /auth/register`
  - `POST /auth/login`
  - `GET /livestock`
- Confirmed normal application behavior

---

### Environment

- macOS (Darwin)
- SQLite
- FastAPI
- SQLAlchemy
- Pydantic v2
