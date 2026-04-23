# Yatube API (v1)

A REST API for the Yatube social blogging platform.  
Supports posts, comments, and groups with Token-based authentication.

---

## Features

- **Posts** — full CRUD; image upload support; author auto-assigned from token
- **Comments** — nested under posts; author-only edit/delete
- **Groups** — read-only catalog
- **Token authentication** — `TokenAuthentication` via `/api/v1/api-token-auth/`
- **Permissions** — authenticated users can write; read-only for anonymous; only the author can modify their own content (`IsAuthorOrReadOnly`)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.9 |
| Framework | Django 3.2, DRF 3.12 |
| Auth | DRF TokenAuthentication |
| Database | SQLite3 |
| Testing | pytest, pytest-django |

---

## Quick Start

```bash
git clone https://github.com/Shipovmax/api_yatube
cd api_yatube

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cd yatube_api
python manage.py migrate
python manage.py runserver
```

API available at `http://127.0.0.1:8000/api/v1/`

---

## Authentication

```http
POST /api/v1/api-token-auth/
Content-Type: application/json

{"username": "user", "password": "password"}
```

Use the returned token in subsequent requests:

```http
Authorization: Token <your_token>
```

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/posts/` | List posts | No |
| `POST` | `/api/v1/posts/` | Create post | Yes |
| `GET/PUT/PATCH/DELETE` | `/api/v1/posts/{id}/` | Post detail | Author only for write |
| `GET` | `/api/v1/groups/` | List groups | Yes |
| `GET` | `/api/v1/groups/{id}/` | Group detail | Yes |
| `GET/POST` | `/api/v1/posts/{id}/comments/` | List / create comments | Yes |
| `GET/PUT/PATCH/DELETE` | `/api/v1/posts/{id}/comments/{id}/` | Comment detail | Author only for write |

---

## Running Tests

```bash
cd api_yatube  # project root
pytest
```

---

## Author

- GitHub: [Shipovmax](https://github.com/Shipovmax)
- Email: shipov.max@icloud.com
