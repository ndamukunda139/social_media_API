# Social Media API

A Django REST API for a social media platform that allows users to create accounts, post content, like posts, follow other users, and receive notifications.

## Features

- **User Management**: Custom user model with bio, profile picture, and following/followers functionality
- **Posts**: Create, read, update, and delete posts with titles and content
- **Comments**: Add comments to posts
- **Likes**: Like posts (unique per user per post)
- **Notifications**: Receive notifications for likes, follows, and other interactions
- **Authentication**: JWT and Token authentication
- **Pagination**: Paginated API responses
- **Filtering and Search**: Filter and search posts and users

## Technologies Used

- **Django 6.0**: Web framework
- **Django REST Framework**: API framework
- **Django REST Framework Simple JWT**: JWT authentication
- **Django Filters**: Filtering for API views
- **Whitenoise**: Static file serving
- **SQLite**: Database (configurable for PostgreSQL)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get tokens
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user (own profile)
- `POST /api/users/{id}/follow/` - Follow a user
- `DELETE /api/users/{id}/unfollow/` - Unfollow a user

### Posts
- `GET /api/posts/` - List posts (with filtering and pagination)
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Get post details
- `PUT /api/posts/{id}/` - Update post (author only)
- `DELETE /api/posts/{id}/` - Delete post (author only)
- `POST /api/posts/{id}/like/` - Like a post
- `DELETE /api/posts/{id}/unlike/` - Unlike a post

### Comments
- `GET /api/posts/{post_id}/comments/` - List comments on a post
- `POST /api/posts/{post_id}/comments/` - Add a comment
- `PUT /api/comments/{id}/` - Update comment (author only)
- `DELETE /api/comments/{id}/` - Delete comment (author only)

### Notifications
- `GET /api/notifications/` - List user notifications
- `PUT /api/notifications/{id}/read/` - Mark notification as read

## Configuration

### Environment Variables
Create a `.env` file in the project root with:
```
DJANGO_SECRET_KEY=your-secret-key
DB_USER=your-db-user
DB_PASSWORD=your-db-password
```

### Database
The project uses SQLite by default. To use PostgreSQL, update the `DATABASES` setting in `settings.py`.

### Static Files
Static files are served using Whitenoise. In production, collect static files:
```bash
python manage.py collectstatic
```

## Testing

Run tests with:
```bash
python manage.py test
```

## Deployment

This project is configured for deployment with security settings enabled (SSL redirect, secure cookies, etc.). Ensure `DEBUG=False` in production.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.