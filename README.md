# ✦ Elkroup

A backend API for a social media platform built with Django. Real-time chat, a follow-based feed, likes, comments — built to be consumed by any frontend client.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Django REST Framework |
| Real-time | Django Channels, Daphne (ASGI) |
| Auth | JWT via `djangorestframework-simplejwt` |
| Database | SQLite |
| Cache / pub-sub | Redis |
| Chat UI (dev only) | Django template for testing live chat |

---

## Features

### Auth
- Register and login with email + password
- JWT access/refresh tokens with auto-rotation
- Token blacklisting on logout

### Feed & Posts
- Create posts with text and media (images/video)
- Cursor-based paginated feed
- Explore endpoint (all posts) and personal feed (followed users only)
- Like / unlike toggle
- Threaded comments with nested replies
- Delete your own posts and comments

### Social Graph
- Follow and unfollow users
- Followers / following lists
- Private user profiles

### Real-time Chat
- DMs between two users
- Group chat rooms
- Typing indicators
- Online presence (join/leave events)
- Soft delete messages
- Full message history with cursor pagination

---

## Project Structure

```
.
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── apps/
│   ├── users/       # auth, profiles, follow graph
│   ├── posts/       # posts, likes, comments, feed
│   └── chat/        # rooms, messages, WS consumers, test template
├── manage.py
└── requirements.txt
```

---

## Database Tables

### users\_user
| Column | Type | Notes |
|---|---|---|
| `id` | integer | primary key |
| `email` | varchar | unique — used for login |
| `username` | varchar | unique |
| `bio` | text | optional |
| `avatar` | varchar | file path, optional |
| `is_private` | boolean | default `false` |
| `created_at` | datetime | auto-set on create |

### users\_follow
| Column | Type | Notes |
|---|---|---|
| `id` | integer | primary key |
| `follower_id` | FK → user | the user who follows |
| `following_id` | FK → user | the user being followed |
| `created_at` | datetime | auto-set on create |
| unique together | — | `(follower, following)` |

### posts\_post
| Column | Type | Notes |
|---|---|---|
| `id` | integer | primary key |
| `author_id` | FK → user | |
| `content` | text | |
| `media` | varchar | file path, optional |
| `created_at` | datetime | auto-set on create |
| `updated_at` | datetime | auto-set on update |

### posts\_like
| Column | Type | Notes |
|---|---|---|
| `id` | integer | primary key |
| `user_id` | FK → user | |
| `post_id` | FK → post | |
| unique together | — | `(user, post)` |

### posts\_comment
| Column | Type | Notes |
|---|---|---|
| `id` | integer | primary key |
| `author_id` | FK → user | |
| `post_id` | FK → post | |
| `parent_id` | FK → self | `null` for top-level comments, set for replies |
| `content` | text | |
| `created_at` | datetime | auto-set on create |

### chat\_room
| Column | Type | Notes |
|---|---|---|
| `id` | integer | primary key |
| `name` | varchar | empty string for DMs |
| `is_dm` | boolean | `true` = direct message, `false` = group |
| `created_by_id` | FK → user | |
| `created_at` | datetime | auto-set on create |

### chat\_message
| Column | Type | Notes |
|---|---|---|
| `id` | integer | primary key |
| `room_id` | FK → room | |
| `sender_id` | FK → user | |
| `content` | text | replaced with `"This message was deleted."` on soft delete |
| `is_deleted` | boolean | default `false` |
| `created_at` | datetime | auto-set on create |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Redis

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/social-app.git
cd social-app

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your secret key

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create a superuser (optional)
python manage.py createsuperuser

# 7. Start Redis
redis-server

# 8. Start the server
DJANGO_SETTINGS_MODULE=config.settings daphne -p 8000 config.asgi:application
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

---

## Testing Live Chat

A minimal Django template is included to test WebSocket chat without any frontend setup.

```
http://127.0.0.1:8000/chat-test/
```

Open the page in two browser tabs, log in as different users, and chat in real time.

---

## API Reference

Two access levels are used across all endpoints:

- `PUBLIC` — no token needed, open to anyone
- `PRIVATE` — must include `Authorization: Bearer <access_token>` in the request header

---

### Auth

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/auth/register/` | `PUBLIC` | Create a new account |
| `POST` | `/api/auth/login/` | `PUBLIC` | Login, returns access + refresh tokens |
| `POST` | `/api/auth/refresh/` | `PUBLIC` | Exchange a refresh token for a new access token |
| `POST` | `/api/auth/logout/` | `PRIVATE` | Invalidate the refresh token |

---

### Users

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/users/me/` | `PRIVATE` | Get your own profile |
| `PATCH` | `/api/users/me/` | `PRIVATE` | Update your bio, avatar, or username |
| `GET` | `/api/users/:username/` | `PRIVATE` | View any user's public profile |
| `POST` | `/api/users/:username/follow/` | `PRIVATE` | Follow or unfollow a user (toggles) |
| `GET` | `/api/users/:username/followers/` | `PRIVATE` | List a user's followers |
| `GET` | `/api/users/:username/following/` | `PRIVATE` | List who a user is following |
| `GET` | `/api/users/:username/posts/` | `PRIVATE` | List all posts by a user |

---

### Posts

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/feed/` | `PRIVATE` | Paginated feed from users you follow |
| `GET` | `/api/explore/` | `PRIVATE` | Paginated feed of all posts |
| `POST` | `/api/posts/` | `PRIVATE` | Create a post — text + optional media file |
| `GET` | `/api/posts/:id/` | `PRIVATE` | Get a single post by id |
| `PATCH` | `/api/posts/:id/` | `PRIVATE` | Edit your post |
| `DELETE` | `/api/posts/:id/` | `PRIVATE` | Delete your post |
| `POST` | `/api/posts/:id/like/` | `PRIVATE` | Like or unlike a post (toggles) |
| `GET` | `/api/posts/:id/comments/` | `PRIVATE` | List comments with nested replies |
| `POST` | `/api/posts/:id/comments/` | `PRIVATE` | Add a comment — include `parent` id for a reply |
| `DELETE` | `/api/comments/:id/` | `PRIVATE` | Delete your comment |

---

### Chat

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/rooms/` | `PRIVATE` | List all rooms you're part of |
| `POST` | `/api/rooms/dm/` | `PRIVATE` | Start or retrieve a DM — body: `{ "username": "bob" }` |
| `GET` | `/api/rooms/:id/messages/` | `PRIVATE` | Paginated message history for a room |

---

### WebSocket

Connect with your access token in the query string — no extra header needed:

```
ws://localhost:8000/ws/chat/:room_id/?token=<access_token>
```

**Client → Server:**

```json
{ "type": "message", "content": "hello!" }
{ "type": "typing",  "is_typing": true }
{ "type": "read",    "message_id": 42 }
{ "type": "delete",  "message_id": 42 }
```

**Server → Client:**

```json
{ "type": "message",  "id": 1, "content": "hello!", "sender_username": "alice", "created_at": "..." }
{ "type": "typing",   "username": "alice", "is_typing": true }
{ "type": "presence", "username": "alice", "online": true }
{ "type": "deleted",  "message_id": 42 }
```