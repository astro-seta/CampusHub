# CampusHUB

A Django web app for managing university clubs and events.
ITEC320

By:
Rodion Reznichenko, 22702601
Setayesh Vahidpour, 22902365

---

## How to Run

1. Install requirements:
```bash
pip install django pillow
```

2. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Start the server:
```bash
python manage.py runserver
```

4. Open browser and go to `http://127.0.0.1:8000/`

---

## User Roles

**Student** (default when you register)
- View clubs and events
- Join/leave clubs
- Register for events

**Club Manager** (assigned by admin)
- Create and manage their own clubs
- Create and manage events for their clubs
- View member and participant lists

**Admin**
- Approve or reject clubs
- Manage users and change their roles
- Delete any club or event

---

## Features

- User registration, login, logout, profile edit with photo upload
- Club list, club detail, join/leave club, club search
- Event list, event detail, event registration with capacity limit
- No duplicate registrations allowed
- Club manager dashboard
- Admin dashboard with pending clubs, all users, all events
- File uploads for profile pictures and club logos
