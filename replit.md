# MiniMonde - Architecture Guide

## Overview

MiniMonde is a kid-friendly blog application built with Flask, designed for children and their parents to share stories and adventures. The application features a colorful, playful interface with French language support and emoji-rich categorization system.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Form Handling**: WTForms with Flask-WTF for CSRF protection
- **Template Engine**: Jinja2 (Flask's default)
- **Session Management**: Flask's built-in session handling with secret key

### Frontend Architecture
- **Template System**: Server-side rendering with Jinja2 templates
- **CSS Framework**: Bootstrap 5.3.0 for responsive design
- **Custom Styling**: CSS3 with CSS variables for theming
- **JavaScript**: Vanilla JavaScript for interactive features
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Fredoka One for headings, Quicksand for body text)

### Data Storage
- **Default Database**: SQLite (development)
- **Production Support**: Configurable via DATABASE_URL environment variable
- **Connection Pooling**: Enabled with pre-ping and 300-second recycle time

## Key Components

### Models (`models.py`)
- **Post Model**: Core blog post entity with fields:
  - id (primary key)
  - title (string, max 200 chars)
  - content (text)
  - category (string, max 50 chars)
  - image_url (optional, max 500 chars)
  - created_at (datetime, auto-generated)
- **Helper Properties**: category_emoji and formatted_date for UI display

### Forms (`forms.py`)
- **PostForm**: WTForms-based form with French language validation
- **Field Validation**: DataRequired, Length, Optional, URL validators
- **Categories**: Predefined choices with emoji representation
- **User-Friendly**: French error messages and helpful placeholders

### Views (`app.py`)
- **Index Route**: Homepage displaying posts in reverse chronological order
- **Create Post Route**: GET/POST handler for new post creation
- **Error Handling**: Flash messages for user feedback

### Templates
- **Base Template**: Common layout with navigation, Bootstrap, and custom CSS
- **Index Template**: Homepage with hero section and post grid
- **Create Post Template**: Form interface for content creation
- **Post Detail Template**: Full post view with sharing features

## Data Flow

1. **Post Creation**:
   - User submits form via `/create` endpoint
   - WTForms validates input data
   - SQLAlchemy saves validated post to database
   - User redirected to homepage with success message

2. **Post Display**:
   - Homepage queries all posts ordered by creation date
   - Template renders posts in responsive card grid
   - Images loaded lazily for performance

3. **Data Persistence**:
   - SQLAlchemy handles database operations
   - Automatic table creation on app startup
   - Connection pooling for production reliability

## External Dependencies

### CDN Resources
- Bootstrap 5.3.0 (CSS framework)
- Font Awesome 6.4.0 (icons)
- Google Fonts (Fredoka One, Quicksand)

### Python Packages
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-WTF (form handling)
- WTForms (form validation)
- Werkzeug (WSGI utilities)

### Environment Configuration
- `SESSION_SECRET`: Flask session encryption key
- `DATABASE_URL`: Database connection string (defaults to SQLite)

## Deployment Strategy

### Development Setup
- Entry point: `main.py` runs Flask development server
- Debug mode enabled for development
- SQLite database for local development
- Host: 0.0.0.0, Port: 5000

### Production Considerations
- ProxyFix middleware configured for reverse proxy deployment
- Environment-based configuration for secrets and database
- Database connection pooling configured
- Static file serving via Flask (consider CDN for production)

### Security Features
- CSRF protection via Flask-WTF
- URL validation for image links
- Input sanitization through WTForms validators
- Session secret key configuration

## Changelog
- July 08, 2025: Initial setup with full blog functionality
- July 08, 2025: Added edit and delete functionality for posts with confirmation modals
- July 08, 2025: Changed blog title from "Mon Blog Magique" to "L'Entre-pote"
- July 08, 2025: Updated blog title to "MiniMondo"
- July 08, 2025: Changed blog title to "MiniMonde"
- July 08, 2025: Removed rainbow icon from navigation brand
- July 08, 2025: Removed rainbow emoji from homepage text and console messages

## User Preferences

Preferred communication style: Simple, everyday language.