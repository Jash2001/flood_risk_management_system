# Flood Risk Emergency Management System

## Project Overview

This application is a web-based Emergency Management and Flood Risk Assessment System developed for a district government. The system enables emergency responders, NGOs, and command center officials to collaboratively monitor flood risk zones and manage real-time incident reporting during heavy rainfall scenarios.

The platform integrates Geographic Information System (GIS) capabilities to support spatial visualization, risk assessment, and operational decision-making.

---

## Problem Statement

Heavy rainfall is forecasted for the upcoming week. Emergency coordinators require a centralized system that:

* Visualizes flood risk zones on an interactive map
* Allows field responders to report incidents
* Enables command center officials to verify and manage incidents
* Supports simultaneous multi-user access
* Provides spatial filtering and risk-based analysis

---

## Key Features

### 1. GIS-Based Flood Zone Visualization

* Displays flood risk zones (High / Medium / Low) using GeoJSON
* Color-coded risk levels
* Interactive popups showing zone details

### 2. Role-Based Access Control

* **Field Responder / NGO**

  * Can create new incident reports by clicking on the map
* **Command Center**

  * Can update incident status (Verified, In Progress, Resolved, Rejected)
* Secure JWT-based authentication

### 3. Incident Management

* Create incident with:

  * Location (GeoJSON Point)
  * Severity
  * Description
* Status updating workflow : REPORTED → VERIFIED → IN_PROGRESS → RESOLVED / REJECTED

### 4. Risk-Based Filtering

* Filter incidents based on selected flood risk zone
* Spatially aware filtering using GIS backend logic

### 5. Dockerized Architecture

* Separate frontend and backend services
* Modular Docker Compose setup
* Single-command orchestration available

---

## Tech Stack

### Backend

* Django
* Django REST Framework
* GeoDjango
* PostgreSQL / PostGIS
* SimpleJWT Authentication
* Docker

### Frontend

* Angular + Ionic
* Leaflet.js for GIS visualization
* OpenStreetMap tiles
* Docker

---

## System Architecture

* Frontend (Angular/Ionic) communicates with Backend REST API
* Backend handles:

  * Authentication
  * GeoJSON processing
  * Incident CRUD operations
  * Role-based permissions
* PostGIS stores spatial data

---

## How to Run the Application

### Prerequisites

* Docker
* Docker Compose
* PostgreSQL / PostGIS

---
### Step 1 : Install PostgreSQL and PostGIS. For postgres user (root user) which is created during the installation set password as root@123 during installation. Make sure to install PostGIS tool once PostgreSQL installation is completed (It will be prompted automatically). 

---
### Step 2: 
### Option 1: Run Using Root-Level Orchestration (Recommended)

From project root:

```
docker compose up --build 
```

---

### Option 2: Run Services Separately

#### Start Backend

```
cd backend
docker compose up --build
```

#### Start Frontend

```
cd frontend
docker compose up --build
```

---

### Step 3: Run the migrations, Collect the static files for Django Admin access and Create Superuser (admin)
```
docker exec -it flood_web bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

---

### Access Application

* Frontend: [http://localhost:8100](http://localhost:8100)
* Backend API: [http://localhost:8000](http://localhost:8000)

---

## User Workflow

In Django Admin (http://localhost:8000/admin) :

1. Users can be created in User section
2. Roles can be mapped to the user in User Profile section
3. Flood Zones can be created on Flood zones section

In Application :

1. User logs in based on role
2. Flood zones are displayed on map
3. Field responders click on map to report incidents
4. Command center verifies and updates incident status
5. Incidents are visualized dynamically with status-based colors

---

## Security Considerations

* JWT Authentication
* Role-based authorization
* Controlled status update permissions

---

## Use Cases

* Disaster preparedness planning
* Real-time flood monitoring
* NGO coordination during emergencies
* Command center incident management

---

## Conclusion

This system provides a scalable, GIS-enabled emergency response platform designed to support multi-level coordination during flood events. The modular Dockerized setup ensures easy deployment and maintenance while supporting simultaneous usage by multiple stakeholders.
