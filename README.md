# SafeNotes API

Сервис приватных заметок с регистрацией, Argon2 и JWT.

Скопируй `.env.example` в `.env`, замени `SECRET_KEY`, затем запусти:

```bash
uv sync --dev
uv run fastapi dev app/main.py
```

Проверяй OAuth2 через кнопку **Authorize** в `/docs` и командой `uv run pytest`.
