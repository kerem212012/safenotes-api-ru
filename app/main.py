from fastapi import FastAPI

app = FastAPI(title="SafeNotes API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Add users, password hashing, JWT login, and owner-scoped notes.
