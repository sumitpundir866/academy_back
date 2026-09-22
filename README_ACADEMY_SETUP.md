# Indian Sports Academy Backend Setup

This backend has been configured to support the Angular frontend for the Indian Sports Academy website.

## New API Endpoints

### Academy Routes (prefix: `/api/academy`)

#### Home
- `GET /api/academy/home/content` - Get home page content (features and classes)

#### Classes
- `GET /api/academy/classes` - Get all active classes
- `POST /api/academy/classes` - Create a new class

#### Team
- `GET /api/academy/team` - Get all active team members
- `POST /api/academy/team` - Create a new team member

#### Gallery
- `GET /api/academy/gallery` - Get all active gallery images
- `GET /api/academy/gallery/{category}` - Get gallery images by category
- `POST /api/academy/gallery` - Create a new gallery image

#### About
- `GET /api/academy/about` - Get about information
- `POST /api/academy/about` - Create about information

#### Contact
- `GET /api/academy/contact` - Get contact information
- `POST /api/academy/contact` - Create contact information

## Database Models

New models have been created in `app/models/academy_models.py`:
- `ClassInfo` - For karate classes information
- `TeamMember` - For team/trainer information
- `GalleryImage` - For gallery images with categories
- `AboutInfo` - For about page content
- `ContactInfo` - For contact details

## Pydantic Schemas

Request/response schemas are defined in `app/pydantic_schemas/academy_schemas.py`.

## CORS Configuration

CORS has been configured to allow requests from:
- `http://localhost:4200` (Angular development server)
- `http://127.0.0.1:4200`

## Database Migration

A migration file has been created at `alembic_versions/academy_models_migration.py`. 
To apply the migration:

```bash
cd d:/sumit/bckend
alembic upgrade head
```

## Running the Server

```bash
cd d:/sumit/bckend
python main.py
```

The server will start on `http://localhost:8000` with API documentation at `http://localhost:8000/docs`

## Frontend Integration

The Angular frontend can now make requests to the backend API endpoints. Example:

```typescript
// Get home content
this.http.get('http://localhost:8000/api/academy/home/content')

// Get classes
this.http.get('http://localhost:8000/api/academy/classes')
```

## Static Content

The home endpoint returns static content that matches the frontend structure:
- Features section with trainer, pricing, and approach information
- Classes section with age-appropriate karate programs
