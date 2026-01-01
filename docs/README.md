# Hotel Grand Documentation Index

Welcome to the Hotel Grand project documentation system. This documentation provides comprehensive coverage of the codebase, architecture, and data flows.

## 📚 Documentation Structure

### Quick Navigation

- [Architecture Overview](#architecture-overview) - System design and module organization
- [Data Flow](#data-flow) - How data moves through the system
- [Module Documentation](#module-documentation) - Detailed docs for each app
- [Configuration Files](#configuration-files) - Settings and URL routing

---

## 🏗️ Architecture Overview

**File:** [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md)

Comprehensive overview of the Hotel Grand system architecture including:

- System architecture diagram
- Module structure and responsibilities
- Data model relationships
- Request/response flows
- Security features
- Deployment considerations

**Key Sections:**

- 4 main application modules
- 5-layer architecture (Client → Django → Application → Models → Data)
- Database schema overview
- File storage structure
- Development workflow

---

## 🔄 Data Flow Documentation

**File:** [`docs/DATA_FLOW.md`](./DATA_FLOW.md)

End-to-end data flow documentation showing how data moves through the system:

- User registration & authentication flow
- Room booking process
- Food ordering flow
- Room review & rating system
- Profile update operations
- Availability checking
- Database operations and file storage
- Error handling flows

**Includes:**

- Sequence diagrams for major operations
- Data input/output by module
- HTTP request/response examples
- Database operation examples
- Performance considerations

---

## 📖 Module Documentation

### Accounts Module

User authentication and profile management

**Model Documentation:**

- [`accounts/models.py.md`](./accounts/models.py.md) - UserProfile model

**View Documentation:**

- [`accounts/views.py.md`](./accounts/views.py.md) - Registration, login, profile management

**Form Documentation:**

- [`accounts/forms.py.md`](./accounts/forms.py.md) - ProfileEditForm

**URL Configuration:**

- [`accounts/urls.py.md`](./accounts/urls.py.md) - Account routing endpoints

---

### Booking Module

Room management and reservation system

**Model Documentation:**

- [`booking/models.py.md`](./booking/models.py.md) - Room, Booking, RoomImage, Review models

**View Documentation:**

- [`booking/views.py.md`](./booking/views.py.md) - Booking operations, availability, reviews

**Form Documentation:**

- [`booking/forms.py.md`](./booking/forms.py.md) - PrivateBookingForm, AvailabilityForm, conflict detection

**No URL Documentation:** Booking URLs included in main hotelgrand/urls.py

---

### Menu Module

Food service and ordering system

**Model Documentation:**

- [`menu/models.py.md`](./menu/models.py.md) - MenuItem, Category, Rating, Order models

**View Documentation:**

- [`menu/views.py.md`](./menu/views.py.md) - Menu display, order placement

**URL Configuration:**

- [`menu/urls.py.md`](./menu/urls.py.md) - Menu routing endpoints

---

### Core Module

Public-facing pages and utilities

**View Documentation:**

- [`core/views.py.md`](./core/views.py.md) - Home, about, public browsing pages

**Model Documentation:**

- [`core/models.py.md`](./core/models.py.md) - Empty (placeholder for future models)

---

## ⚙️ Configuration Files

### Project Settings

**File:** [`hotelgrand/settings.py.md`](./hotelgrand/settings.py.md)

Django configuration including:

- Debug and security settings
- Installed applications (4 custom + 6 Django apps)
- Middleware stack (7 components)
- Database configuration (MySQL)
- Template configuration
- CSRF and auth settings

---

### URL Routing

**File:** [`hotelgrand/urls.py.md`](./hotelgrand/urls.py.md)

Main URL dispatcher mapping requests to views:

- Admin panel
- Public endpoints (home, about, rooms, menu)
- Authentication routes (login, logout)
- App inclusion (accounts, booking, menu)
- Static/media file serving (development)

---

## 📋 Documentation Map

```
docs/
├── README.md (this file)
├── ARCHITECTURE.md
├── DATA_FLOW.md
│
├── accounts/
│   ├── models.py.md
│   ├── views.py.md
│   ├── forms.py.md
│   └── urls.py.md
│
├── booking/
│   ├── models.py.md
│   ├── views.py.md
│   └── forms.py.md
│
├── menu/
│   ├── models.py.md
│   ├── views.py.md
│   └── urls.py.md
│
├── core/
│   ├── models.py.md
│   └── views.py.md
│
└── hotelgrand/
    ├── settings.py.md
    └── urls.py.md
```

---

## 🎯 How to Use This Documentation

### For New Developers

1. **Start here:** Read [`ARCHITECTURE.md`](./ARCHITECTURE.md) for system overview
2. **Understand flows:** Study [`DATA_FLOW.md`](./DATA_FLOW.md)
3. **Dive deep:** Read individual module documentation
4. **Configuration:** Check [`hotelgrand/settings.py.md`](./hotelgrand/settings.py.md) for Django setup

### For Understanding a Specific Feature

1. **Room Booking:** See [`booking/models.py.md`](./booking/models.py.md) and [`booking/views.py.md`](./booking/views.py.md)
2. **User Accounts:** See [`accounts/models.py.md`](./accounts/models.py.md) and [`accounts/views.py.md`](./accounts/views.py.md)
3. **Food Ordering:** See [`menu/models.py.md`](./menu/models.py.md) and [`menu/views.py.md`](./menu/views.py.md)

### For Understanding Data Flow

- **Booking process:** See [`DATA_FLOW.md`](./DATA_FLOW.md) section "Room Booking Flow"
- **Order placement:** See [`DATA_FLOW.md`](./DATA_FLOW.md) section "Food Order Flow"
- **Authentication:** See [`DATA_FLOW.md`](./DATA_FLOW.md) section "User Registration & Authentication Flow"

### For Configuration Questions

- **What apps are installed?** See [`hotelgrand/settings.py.md`](./hotelgrand/settings.py.md)
- **What URLs are available?** See [`hotelgrand/urls.py.md`](./hotelgrand/urls.py.md)
- **How is database configured?** See [`hotelgrand/settings.py.md`](./hotelgrand/settings.py.md)

---

## 🔍 Key Concepts

### Models & Database

- **User Management:** Django's User + custom UserProfile
- **Room Management:** Room, RoomImage (multiple images per room)
- **Bookings:** Booking with auto-calculated pricing based on duration
- **Reviews:** Guest reviews for rooms with ratings
- **Food Service:** MenuItem (with category), Order, Rating

### Views & Business Logic

- **Public Views:** Home, about, room catalog, menu catalog (no auth required)
- **Protected Views:** Private booking, food ordering, reviews (login required)
- **Admin Interface:** Django admin for database management

### Forms & Validation

- **Booking Validation:** Date range checking, room conflict detection
- **Profile Forms:** Image upload, password hashing
- **Availability Filtering:** Date-based room search

### Security

- Authentication: Django's built-in auth system
- CSRF Protection: Middleware + token validation
- Password Security: Hashing with Django's password hasher

---

## 📊 Data Models Summary

### User-Related

```
User (Django)
  ├── id, username, email, password
  └── UserProfile (One-to-One)
      ├── role (customer/worker)
      ├── profile_image
      ├── loyalty_points
      ├── dob, phone, address
      └── Methods: age, completion_percent()
```

### Room-Related

```
Room
  ├── name, description, price, capacity
  ├── bedrooms, bathrooms, size
  └── images (One-to-Many: RoomImage)

RoomImage
  ├── image or image_url
  ├── caption, link_url
  └── get_image_source()

Booking
  ├── room (FK)
  ├── guest_name, check_in, check_out
  ├── status, special_requests
  ├── total_price (auto-calculated)
  ├── rating, review
  └── save() auto-calculates price

Review
  ├── room (FK), user (FK)
  ├── text, rating
  └── created_at (auto)
```

### Food-Related

```
Category
  ├── name, description
  └── items (One-to-Many: MenuItem)

MenuItem
  ├── category (FK)
  ├── name, description, price
  ├── estimated_time, loyalty_points
  ├── image or image_url
  └── average_rating()

Rating
  ├── menu_item (FK), user (FK)
  └── value (1-5)

Order
  ├── user (FK), booking (FK)
  ├── item (FK), quantity
  ├── ordered_at, status
  └── status: pending → preparing → delivered
```

---

## 🔗 Relationships & Foreign Keys

**User Relationships:**

- User ←→ UserProfile (OneToOne)
- User → Review (many, writes reviews)
- User → Rating (many, rates items)
- User → Order (many, places orders)

**Room Relationships:**

- Room → Booking (many)
- Room → RoomImage (many)
- Room → Review (many)

**Booking Relationships:**

- Booking → Order (many, contains orders)
- Booking ← Review (linked via Booking in data flow)

**Menu Relationships:**

- Category → MenuItem (many)
- MenuItem → Rating (many)
- MenuItem → Order (many)

---

## 🚀 Endpoints Summary

### Public Endpoints

```
GET  /                    Home page
GET  /about/             About page
GET  /rooms/             Room catalog (paginated)
GET  /menu/              Menu catalog (paginated)
```

### Authentication

```
GET/POST /login/         User login
GET      /logout/        User logout
POST     /accounts/register/   User registration
```

### User Account (Login Required)

```
GET/POST /accounts/edit/           Edit profile
POST     /accounts/update/username/ Update username
POST     /accounts/update/email/    Update email
POST     /accounts/update/photo/    Upload profile picture
POST     /accounts/update/password/ Change password
POST     /accounts/update/details/  Update personal info
```

### Room Booking (Login Required)

```
GET/POST /book/private/        Private booking with filters
POST     /book/check/          Check availability
GET      /book/booking/success/ Booking confirmation
GET      /book/room/<id>/      Room details & reviews
POST     /book/extend-booking/ Extend existing booking
POST     /book/submit-review/  Submit room review
```

### Food Menu (Login + Checked-in Required)

```
GET      /menu/private-menu/   View menu (must be checked-in)
POST     /menu/place-order/    Place food order
```

---

## 🔐 Security Features

- **Authentication:** Django's user authentication system
- **CSRF Protection:** Middleware + token validation in forms
- **Password Security:** PBKDF2 hashing, validation on registration
- **SQL Injection:** Protected by Django ORM
- **Authorization:** login_required decorator on protected views
- **Role-Based:** UserProfile.role field (customer/worker)

---

## ⚠️ Important Notes

### Development Only

- `DEBUG = True` (must be False in production)
- `SECRET_KEY` is insecure (change in production)
- `ALLOWED_HOSTS` is empty (specify domains in production)
- Media files served by Django (use nginx/Apache in production)

### Current Limitations

- No REST API (web-only)
- No async task queue
- No caching layer
- No email notifications
- Local filesystem storage only
- Single MySQL database instance

### Database

- **Engine:** MySQL
- **Database:** hotelgrand_db
- **User:** django_user
- **Host:** localhost (default)
- **Ensure:** Database and user created before running

---

## 📝 Documentation Format

Each file follows a consistent 8-section structure:

1. **Overview** - Purpose and responsibility
2. **File Location** - Path in project
3. **Key Components** - Classes, functions, variables
4. **Execution Flow** - Step-by-step process
5. **Data Flow** - Inputs, processing, outputs
6. **Mermaid Diagrams** - Visual representations
7. **Error Handling & Edge Cases** - Failures and special cases
8. **Example Usage** - Code samples

---

## 🎓 Learning Path

**Beginner → Intermediate → Advanced**

### Level 1: Overview

1. Read [`ARCHITECTURE.md`](./ARCHITECTURE.md) to understand system layout
2. Skim [`DATA_FLOW.md`](./DATA_FLOW.md) for high-level flows
3. Check [`hotelgrand/urls.py.md`](./hotelgrand/urls.py.md) for available endpoints

### Level 2: Core Features

1. Study [`booking/models.py.md`](./booking/models.py.md) for data structures
2. Read [`booking/views.py.md`](./booking/views.py.md) for business logic
3. Learn [`accounts/models.py.md`](./accounts/models.py.md) for user system

### Level 3: Advanced Topics

1. Deep dive into [`booking/views.py.md`](./booking/views.py.md) for conflict detection
2. Study [`DATA_FLOW.md`](./DATA_FLOW.md) for complete request cycles
3. Review [`hotelgrand/settings.py.md`](./hotelgrand/settings.py.md) for configuration details

---

## 🔧 Quick Reference

### File Organization

```
hotelgrand/              # Main project folder
├── accounts/            # User account management
├── booking/             # Room booking system
├── menu/                # Food ordering
├── core/                # Public pages
├── hotelgrand/          # Project settings
├── templates/           # HTML templates
├── media/               # User uploads
├── static/              # Static files
└── manage.py            # Django management
```

### Key Technologies

- **Framework:** Django 5.2.4
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Django's built-in system
- **Forms:** Django ModelForms

---

## 📞 Getting Help

### For Understanding a Feature

1. Find it in the architecture diagram ([`ARCHITECTURE.md`](./ARCHITECTURE.md))
2. Read the relevant module documentation
3. Check [`DATA_FLOW.md`](./DATA_FLOW.md) for the complete flow
4. Look at example usage section in module docs

### For Understanding Code Flow

1. Find the view in [`hotelgrand/urls.py.md`](./hotelgrand/urls.py.md)
2. Read the view documentation (e.g., [`booking/views.py.md`](./booking/views.py.md))
3. Check the models documentation for data structures
4. Review data flow section in [`DATA_FLOW.md`](./DATA_FLOW.md)

### For Configuration Questions

- Database: [`hotelgrand/settings.py.md`](./hotelgrand/settings.py.md)
- URLs: [`hotelgrand/urls.py.md`](./hotelgrand/urls.py.md)
- Apps: [`ARCHITECTURE.md`](./ARCHITECTURE.md) → Module Structure

---

## 📖 Complete File Index

| File                        | Type   | Purpose                          |
| --------------------------- | ------ | -------------------------------- |
| `ARCHITECTURE.md`           | System | Overall architecture and design  |
| `DATA_FLOW.md`              | System | Data movement and processing     |
| `accounts/models.py.md`     | Module | User profile data model          |
| `accounts/views.py.md`      | Module | Authentication and profile views |
| `accounts/forms.py.md`      | Module | Profile editing form             |
| `accounts/urls.py.md`       | Module | Account URL routing              |
| `booking/models.py.md`      | Module | Room and booking data models     |
| `booking/views.py.md`       | Module | Booking and availability logic   |
| `booking/forms.py.md`       | Module | Booking and search forms         |
| `menu/models.py.md`         | Module | Food and order data models       |
| `menu/views.py.md`          | Module | Menu and ordering views          |
| `menu/urls.py.md`           | Module | Menu URL routing                 |
| `core/models.py.md`         | Module | Core model (empty)               |
| `core/views.py.md`          | Module | Public page views                |
| `hotelgrand/settings.py.md` | Config | Django settings                  |
| `hotelgrand/urls.py.md`     | Config | Main URL dispatcher              |

---

## ✅ Last Updated

Documentation created: January 2025

Covers:

- Django 5.2.4
- Hotel Grand v1.0
- 4 application modules
- All models, views, forms, and URLs

---

**Happy coding! 🚀**
