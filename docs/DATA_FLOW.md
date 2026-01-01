# Data Flow Documentation

## Overview

This document describes the end-to-end data flow across all major system operations in Hotel Grand. It traces how data moves through the application layers from user input to database persistence and back to display.

## Complete Data Flow Diagrams

### 1. User Registration & Authentication Flow

```mermaid
sequenceDiagram
    Actor User
    participant Browser
    participant Views as accounts/views.py
    participant Forms as accounts/forms.py
    participant Models as Django Models
    participant DB as MySQL Database

    User->>Browser: Enter registration data
    Browser->>Views: POST /accounts/register/<br/>{username, email, pwd1, pwd2}
    
    Views->>Views: Extract form data
    Views->>Views: Validate passwords match
    Views->>Views: Check username unique
    Views->>Views: Check email unique
    
    Views->>Models: User.objects.create_user()<br/>(username, email, password)
    Models->>DB: INSERT INTO auth_user
    
    Views->>Models: UserProfile.objects.create()<br/>(user, role='customer')
    Models->>DB: INSERT INTO accounts_userprofile
    
    Models-->>Views: UserProfile instance
    Views-->>Browser: JSON {success: true}
    Browser-->>User: Show login page
    
    User->>Browser: Enter credentials
    Browser->>Views: POST /accounts/login/<br/>{username, password}
    
    Views->>Views: Django authenticate()
    Views->>Models: User.objects.get()
    Models->>DB: SELECT * FROM auth_user
    
    DB-->>Models: User instance
    Models-->>Views: User object
    Views->>Views: Check password_hash
    
    Views->>Views: login() creates session
    Views-->>Browser: JSON {success: true}
    Browser-->>User: Redirect to dashboard
```

### 2. Room Booking Flow

```mermaid
graph TD
    A["User Views Rooms"] -->|GET /rooms/| B["core.views.public_booking"]
    B -->|Query| C["Room.objects.all"]
    C -->|Read| D["[Room1, Room2, ...]"]
    
    E["User Selects Room"] -->|POST /book/private/| F["booking.views.private_booking"]
    F -->|Parse| G["check_in, check_out, room_id"]
    
    G -->|Query Conflicts| H["Booking.objects.filter<br/>overlapping dates"]
    H -->|Read| I["DB: hotelgrand_db"]
    I -->|conflicts?| J{Conflict<br/>Found?}
    
    J -->|Yes| K["Error Message"]
    K -->|Redirect| L["booking page"]
    
    J -->|No| M["Create Booking<br/>object"]
    M -->|Auto-calc<br/>total_price| N["price × duration"]
    N -->|Save| O["Booking.save()"]
    O -->|Write| P["INSERT INTO<br/>booking_booking"]
    
    P -->|Success| Q["Redirect Success"]
    Q -->|Message| R["booking_success"]
    R -->|HTML| S["User Confirmation"]
```

### 3. Food Order Flow

```mermaid
sequenceDiagram
    Actor Guest
    participant Browser
    participant Views as menu/views.py
    participant Models as Django Models
    participant DB as MySQL

    Guest->>Browser: GET /menu/private-menu/
    Browser->>Views: HTTP Request
    Views->>Views: Check login_required
    Views->>Models: Booking.objects.filter()<br/>guest_name=user.username
    Models->>DB: SELECT * FROM booking_booking<br/>WHERE guest_name=?
    
    DB-->>Models: [Booking1]
    Models-->>Views: Booking object
    Views->>Views: Check status='checked_in'
    
    Views->>Models: MenuItem.objects.all()
    Models->>DB: SELECT * FROM menu_menuitem
    
    DB-->>Models: [Item1, Item2, ...]
    Models-->>Views: QuerySet of items
    Views-->>Browser: Render menu.html<br/>with items & booking
    Browser-->>Guest: Display menu
    
    Guest->>Browser: Select item, qty=2
    Browser->>Views: POST /menu/place-order/<br/>{item_id: 3, quantity: 2}
    
    Views->>Views: Extract item_id, quantity
    Views->>Models: MenuItem.objects.get(id=3)
    Models->>DB: SELECT * FROM menu_menuitem<br/>WHERE id=3
    
    DB-->>Models: MenuItem
    Models-->>Views: Item object
    
    Views->>Models: Order.objects.create()<br/>user, booking, item, qty
    Models->>DB: INSERT INTO menu_order
    
    DB-->>Models: Order instance
    Models-->>Views: Order created
    Views-->>Browser: JSON {success: true}
    Browser-->>Guest: Success message
```

### 4. Room Review & Rating Flow

```mermaid
graph LR
    A["Guest Checks In"] -->|Auto-update| B["Booking.status<br/>= checked_in"]
    B -->|Saved| C[(Database)]
    
    D["Guest Views Room"] -->|GET /book/room/5/| E["room_detail view"]
    E -->|Query| F["Review.objects.filter<br/>room=5"]
    F -->|Read| C
    C -->|Results| G["[Review1, Review2]"]
    
    H["Guest Submits Review"] -->|POST /book/submit-review/| I["submit_review view"]
    I -->|Verify| J{Booking<br/>checked_in?}
    J -->|No| K["Error message"]
    J -->|Yes| L["Create Review<br/>object"]
    
    L -->|user, room, text, rating| M["Review.objects.create()"]
    M -->|Write| N["INSERT INTO<br/>booking_review"]
    N -->|Saved| C
    
    O["Display Room"] -->|Aggregate| P["Calculate<br/>average_rating"]
    P -->|Sum ratings/count| Q["avg = 4.3"]
    Q -->|Display| R["Room Detail Page"]
```

### 5. Profile Update Flow

```mermaid
sequenceDiagram
    participant User
    participant Form as ProfileEditForm
    participant Save as form.save()
    participant Models as ORM
    participant DB as MySQL

    User->>User: Load edit_profile page
    Form->>Models: UserProfile.objects.get(user=current_user)
    Models->>DB: SELECT from accounts_userprofile
    DB-->>Models: UserProfile instance
    Models-->>Form: Pre-populate form
    Form-->>User: Display form with data
    
    User->>Form: Submit updated data<br/>{username, password, image}
    
    Form->>Form: Validate fields
    Form->>Save: save(commit=False)
    Save->>Models: Create profile_instance (unsaved)
    Save->>Save: Get profile.user
    Save->>Models: Update User.username
    
    alt if password provided
        Save->>Models: user.set_password(pwd_hash)
    end
    
    Save->>Models: user.save()
    Models->>DB: UPDATE auth_user SET username=?
    
    Save->>Models: profile.save()
    Models->>DB: UPDATE accounts_userprofile<br/>SET profile_image=?
    
    DB-->>Models: Rows updated
    Models-->>User: Confirmation
    User->>User: Redirect to dashboard
```

### 6. Availability Check Flow

```mermaid
graph TD
    A["User Searches<br/>check_in, check_out"] -->|POST /book/check/| B["check_availability view"]
    
    B -->|Form validation| C["AvailabilityForm.is_valid()"]
    C -->|Parse| D["dates extracted"]
    
    D -->|Query each room| E["Room.objects.all()"]
    E -->|Read| F[(Database)]
    F -->|Results| G["Room list"]
    
    H["Filter Logic"] -->|For each room| I["Booking.objects.filter"]
    I -->|check_in < user_checkout<br/>check_out > user_checkin<br/>status=confirmed| J["Overlapping?"]
    
    J -->|Yes| K["Room unavailable<br/>Skip"]
    J -->|No| L["Room available<br/>Add to list"]
    
    M["Paginate Results"] -->|9 per page| N["page_obj"]
    N -->|Context| O["Render template"]
    O -->|Display| P["Available rooms"]
```

## Data Input/Output by Module

### Accounts Module

**Inputs:**
```
Registration:
  - username (string, required)
  - email (string, required)
  - password1 (string, required)
  - password2 (string, required)

Login:
  - username (string, required)
  - password (string, required)

Profile Edit:
  - username (string, optional)
  - password (string, optional)
  - profile_image (file, optional)
  - dob (date, optional)
  - phone (string, optional)
  - address (text, optional)
```

**Outputs:**
```
Stored in Database:
  - User record (auth_user table)
  - UserProfile record (accounts_userprofile table)
  - Profile image file (media/profile_images/)
  - Session cookie (for authentication)
```

**Database Operations:**
```
CREATE: User, UserProfile, Profile images
READ: User authentication, profile retrieval
UPDATE: Username, email, password, profile fields
DELETE: User and profile (cascade)
```

---

### Booking Module

**Inputs:**
```
Booking:
  - room_id (integer)
  - check_in (datetime)
  - check_out (datetime)
  - guest_count (integer)
  - special_requests (text, optional)

Availability:
  - check_in (date)
  - check_out (date)

Review:
  - room_id (integer)
  - text (text)
  - rating (integer 1-5, optional)
```

**Outputs:**
```
Stored in Database:
  - Booking record with:
    - status (pending/confirmed/checked_in/completed)
    - total_price (auto-calculated)
  - Review record linked to booking
  - Room images stored in media/room_images/

Display Data:
  - Available rooms list (paginated)
  - Room details with images & reviews
  - Average ratings calculated from reviews
```

**Database Operations:**
```
CREATE: Booking, Review, RoomImage
READ: Room details, availability checking, reviews
UPDATE: Booking status, total_price recalculation, booking extension
DELETE: Bookings, reviews (with cascade)
```

**Price Calculation:**
```
total_price = room.price × max(days_between_dates, 1)
- Handles fractional days via Decimal precision
- Recalculated on each booking.save()
```

---

### Menu Module

**Inputs:**
```
Order:
  - item_id (integer)
  - quantity (integer)
  - [user_id, booking_id auto-populated from session]

Rating:
  - menu_item_id (integer)
  - value (integer 1-5)
  - [user_id auto-populated from session]
```

**Outputs:**
```
Stored in Database:
  - Order record with:
    - status (pending/preparing/delivered)
    - ordered_at (auto timestamp)
  - Rating record
  - Menu images in media/menu_images/

Display Data:
  - Menu items with:
    - Average rating (calculated on-demand)
    - Category grouping
    - Price and details
```

**Database Operations:**
```
CREATE: Order, Rating
READ: MenuItem, Category, Order history
UPDATE: Order status, MenuItem rating aggregation
DELETE: Orders, ratings (with cascade)
```

**Rating Aggregation:**
```
average_rating = Sum(all_ratings) / Count(all_ratings)
- Calculated on each access (no caching)
- Returns 0 if no ratings exist
- Rounded to 1 decimal place
```

---

### Core Module

**Inputs:**
```
GET parameters:
  - page (optional, for pagination)
```

**Outputs:**
```
Display Data:
  - Home page (static template)
  - About page (static template)
  - Public room catalog (paginated, 9/page)
  - Public menu (paginated, 3/page)
  - Category list for menu
```

**Database Operations:**
```
READ: Room.objects.all()
      MenuItem.objects.all()
      Category.objects.prefetch_related('items')
      (No writes)
```

---

## Request/Response Cycle with Data

### Complete HTTP Request Example

**Request: User Books Room**
```http
POST /book/private/ HTTP/1.1
Host: hotelgrand.local
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123xyz

room_id=5&check_in=2024-03-15T15:00&check_out=2024-03-18T11:00&guest_count=2&special_requests=Late+checkout
```

**Data Processing:**
```
1. URL Router matches /book/private/ → booking.views.private_booking
2. Middleware chain:
   - Session: Load session, get request.user
   - Auth: Populate request.user with authenticated User
   - CSRF: Validate CSRF token
3. View extracts POST data:
   - room_id = 5
   - check_in = datetime(2024, 3, 15, 15, 0)
   - check_out = datetime(2024, 3, 18, 11, 0)
   - guest_count = 2
4. Query: SELECT * FROM booking_booking WHERE room_id=5 AND ... (overlap check)
5. Calculate: total_price = 150.00 * 3 days = 450.00
6. Create: INSERT INTO booking_booking (room_id, guest_name, check_in, check_out, total_price, status)
7. Response: Redirect to /book/booking/success/
```

**Response:**
```http
HTTP/1.1 302 Found
Location: /book/booking/success/
Set-Cookie: messages=...
```

### Complete Database Example

**Tables Involved in Booking:**
```
auth_user
├── id, username, email, password, ...
└── Used for: User authentication

accounts_userprofile
├── id, user_id (FK), role, loyalty_points, ...
└── Used for: Profile details

booking_room
├── id, name, price, capacity, ...
└── Used for: Room details, pricing

booking_booking
├── id, room_id (FK), guest_name, check_in, check_out, total_price, status, ...
└── Used for: Reservation tracking

booking_review
├── id, room_id (FK), user_id (FK), text, rating, ...
└── Used for: Guest feedback
```

**Sample Data Flow:**
```
User Request → Load Room (booking_room) → Check conflicts (query booking_booking)
            → Calculate price
            → Insert new Booking (booking_booking)
            → Commit transaction
            → Return confirmation
```

## Caching & Performance Considerations

### Current Implementation (No Caching)
- All queries hit database directly
- MenuItem.average_rating() recalculated each access
- Room availability filtered for each request
- No query result caching

### Data Access Patterns

**Hot Paths (Frequent Access):**
1. Room listing - public_booking view (accessed by every guest)
2. Menu listing - public_menu view (accessed by every guest)
3. Availability check - frequent during booking season
4. Room detail - accessed per user interest

**Optimization Opportunities:**
```python
# Example: Add select_related for foreign keys
reviews = Review.objects.select_related('user', 'room')

# Example: Prefetch related data
categories = Category.objects.prefetch_related('items')

# Example: Cache expensive calculations
cache.set(f'room_{room_id}_avg_rating', avg_rating, timeout=3600)
```

## File Storage Data Flow

### Profile Image Upload
```
User → Form (multipart/form-data) → View validates
     → Check old image exists
     → Delete old image from filesystem
     → Save new image to media/profile_images/
     → Store filename in UserProfile.profile_image
     → Commit to database
```

### Room Image Upload
```
Admin → Admin interface
      → Create RoomImage instance
      → Upload via form → Validate (check image_url or image exists)
      → Save image to media/room_images/
      → Store reference in RoomImage model
      → get_image_source() returns correct URL on display
```

## Error Data Flow

### Validation Error Example
```
User submits booking with check_out before check_in
     ↓
Form.clean() validation
     ↓
ValidationError raised with message
     ↓
Form.is_valid() returns False
     ↓
View checks is_valid()
     ↓
Display error message to user
     ↓
Re-render form with errors
```

### Database Constraint Example
```
Try to delete Room with related Bookings
     ↓
Django cascade delete triggered
     ↓
Delete all Booking records for room
     ↓
Delete all Review records for room
     ↓
Delete Room record
     ↓
Commit transaction
```

## Temporal Data Flows

### Booking Status Lifecycle
```
Timeline:
  T1: User creates booking (status='confirmed')
  T2: Guest checks in (status='checked_in')
  T3: Guest checks out (status='completed' via expire_old_bookings)
  T4: Guest submits review (still linked to completed booking)

Data persistence:
  - All status changes tracked in database
  - Historical bookings remain for reporting/reviews
  - Automatic status updates via expire_old_bookings() utility
```

### Order Status Progression
```
Timeline:
  T1: Guest places order (status='pending')
  T2: Staff starts preparing (status='preparing')
  T3: Order ready for delivery (status='delivered')
  T4: Order history available for guest

Data tracking:
  - ordered_at timestamp auto-set
  - Manual status updates (no automation)
  - Queries filter by status for display
```

## External Dependencies & Data Sources

**MySQL Database:**
- Central data store
- All models persisted here
- Django ORM abstraction layer

**File System (Media):**
- Profile images
- Room images
- Menu images
- Served via Django's static file handler (dev only)

**Session Storage:**
- Django session framework (database-backed by default)
- Stores: authentication state, csrf token

## Data Export/Reporting Flows (Potential)

### Booking Report Data
```
Manager queries: Bookings for date range
     ↓
Django ORM: Booking.objects.filter(check_in__gte=start, check_out__lte=end)
     ↓
Database: SELECT with JOINs to Room, User, Review tables
     ↓
Aggregation: Group by room, calculate occupancy, revenue
     ↓
Export: CSV/PDF generation
```

### Revenue Calculation
```
Sum all confirmed/completed bookings: total_price
Filter by date range
Group by room type
Calculate average nightly rate
```

## Data Integrity Constraints

### Foreign Key Relationships
- Booking → Room (cascade delete)
- Review → Room (cascade delete)
- Review → User (cascade delete)
- Order → User (cascade delete)
- Order → Booking (cascade delete)
- Order → MenuItem (cascade delete)

### Uniqueness Constraints
- User.username (enforced by Django)
- User.email (custom validation in register view)
- UserProfile (1:1 with User)

### Validation Rules
- Check_out > check_in (form validation)
- Room availability (booking conflict check)
- At least one image source (RoomImage.clean())
- Quantity ≥ 1 (PositiveIntegerField)

## Summary

Hotel Grand's data flows through a standard Django web application architecture:

1. **User Input** → Form validation
2. **View Processing** → Business logic
3. **Model Operations** → ORM queries
4. **Database Persistence** → MySQL storage
5. **Response Generation** → Template rendering
6. **User Display** → Browser rendering

All data is persisted in a single MySQL database with optional file storage for images. No caching, queuing, or external data sources are currently implemented.
