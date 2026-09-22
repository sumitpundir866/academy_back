
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.academy_models import GalleryImage, GalleryclassVedio, TeamMember, UserPermission
from pydantic import BaseModel
import os
import uuid
import random
import string
import httpx

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = "academy-media"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

router = APIRouter()


# Pydantic models for login
class LoginRequest(BaseModel):
    user_name: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    user_data: dict = None


# Password Change Models
class OTPRequest(BaseModel):
    user_name: str
    mobile_number: str


class PasswordChangeWithOTPRequest(BaseModel):
    user_name: str
    mobile_number: str
    otp: str
    new_password: str


# In-memory OTP storage
otp_storage = {}


def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


async def send_otp_sms(mobile_number: str, otp: str):
    """Send OTP via SMS service"""

    # Method 1: Try Textlocal
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.textlocal.in/send/",
                data={
                    "apikey": "<YOUR_TEXTLOCAL_API_KEY>",
                    "numbers": f"91{mobile_number}",
                    "message": f"Your OTP is: {otp}. Do not share this with anyone. Valid for 5 minutes.",
                    "sender": "TXTLCL"
                }
            )

            result = response.json()

            if result.get("status") == "success":
                print(f"OTP sent via Textlocal to {mobile_number}")
                return True

    except Exception as e:
        print(f"Textlocal failed: {e}")


    # Method 2: Try Fast2SMS
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://www.fast2sms.com/dev/bulkV2",
                params={
                    "authorization": "<YOUR_FAST2SMS_API_KEY>",
                    "route": "v3",
                    "sender_id": "FTWSMS",
                    "message": f"Your OTP is: {otp}. Do not share this with anyone.",
                    "language": "english",
                    "numbers": mobile_number
                }
            )

            if response.status_code == 200:
                print(f"OTP sent via Fast2SMS to {mobile_number}")
                return True

    except Exception as e:
        print(f"Fast2SMS failed: {e}")


    # Method 3: Try MSG91
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://control.msg91.com/api/v5/flow/",
                json={
                    "template_id": "6507b8a1d6fc05565a4c7b8d",
                    "short_url": "1",
                    "mobiles": f"91{mobile_number}",
                    "VAR1": otp,
                    "VAR2": "5"
                },
                headers={
                    "authkey": "<YOUR_MSG91_AUTH_KEY>"
                }
            )

            if response.status_code == 200:
                print(f"OTP sent via MSG91 to {mobile_number}")
                return True

    except Exception as e:
        print(f"MSG91 failed: {e}")


    # Method 4: Try Twilio
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.twilio.com/2010-04-01/Accounts/ACdemo/Messages.json",
                data={
                    "To": f"+91{mobile_number}",
                    "From": "+15017122661",
                    "Body": f"Your OTP is: {otp}. Do not share this with anyone."
                },
                auth=("ACdemo", "demopassword")
            )

            if response.status_code == 201:
                print(f"OTP sent via Twilio to {mobile_number}")
                return True

    except Exception as e:
        print(f"Twilio failed: {e}")


    # Method 5: EngineeringTGR
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://smsapi.engineeringtgr.com/send/",
                params={
                    "apikey": "<YOUR_ENGINEERINGTGR_API_KEY>",
                    "number": f"91{mobile_number}",
                    "message": f"Your OTP is: {otp}. Do not share this with anyone.",
                    "senderid": "IFRWEP"
                }
            )

            if response.status_code == 200:
                print(f"OTP sent via EngineeringTGR to {mobile_number}")
                return True

    except Exception as e:
        print(f"EngineeringTGR failed: {e}")


    print(f"All SMS services failed for {mobile_number}")
    print(f"OTP (for testing): {otp}")

    return True


# Login Endpoint
@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint for users"""

    try:
        user = db.query(UserPermission).filter(
            UserPermission.user_name == login_data.user_name
        ).first()

        if not user:
            return LoginResponse(
                success=False,
                message="User not found"
            )

        if user.password != login_data.password:
            return LoginResponse(
                success=False,
                message="Invalid password"
            )

        return LoginResponse(
            success=True,
            message="Login successful",
            user_data={
                "user_name": user.user_name,
                "user_role": user.user_role,
                "edit": user.edit,
                "delete": user.delete,
                "upload": user.upload
            }
        )

    except Exception as e:
        return LoginResponse(
            success=False,
            message=f"Login error: {str(e)}"
        )


# Generate OTP Endpoint
@router.post("/generate-otp")
async def generate_otp_endpoint(
    otp_request: OTPRequest,
    db: Session = Depends(get_db)
):
    """Generate OTP and send to mobile number"""

    try:
        user = db.query(UserPermission).filter(
            UserPermission.user_name == otp_request.user_name,
            UserPermission.mobile_number == otp_request.mobile_number
        ).first()

        if not user:
            return {
                "success": False,
                "message": "User not found or mobile number does not match"
            }

        otp = generate_otp()

        otp_storage[otp_request.user_name] = {
            "otp": otp,
            "mobile": otp_request.mobile_number,
            "verified": False
        }

        sms_sent = await send_otp_sms(
            otp_request.mobile_number,
            otp
        )

        if sms_sent:
            return {
                "success": True,
                "message": "OTP sent to your mobile number",
                "mobile": otp_request.mobile_number
            }

        return {
            "success": False,
            "message": "Failed to send OTP. Please try again."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating OTP: {str(e)}"
        }


# Change Password with OTP Verification
@router.post("/change-password")
def change_password_with_otp(
    password_request: PasswordChangeWithOTPRequest,
    db: Session = Depends(get_db)
):
    """Verify mobile number, OTP and change password"""

    try:
        if password_request.user_name not in otp_storage:
            return {
                "success": False,
                "message": "Please generate OTP first"
            }

        stored_otp_data = otp_storage[
            password_request.user_name
        ]

        if stored_otp_data["mobile"] != password_request.mobile_number:
            return {
                "success": False,
                "message": "Mobile number does not match"
            }

        if stored_otp_data["otp"] != password_request.otp:
            return {
                "success": False,
                "message": "Invalid OTP"
            }

        user = db.query(UserPermission).filter(
            UserPermission.user_name == password_request.user_name
        ).first()

        if not user:
            return {
                "success": False,
                "message": "User not found"
            }

        user.password = password_request.new_password

        db.commit()

        del otp_storage[password_request.user_name]

        return {
            "success": True,
            "message": "Password changed successfully"
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": f"Error changing password: {str(e)}"
        }


# ============================================================
# GALLERY IMAGE UPLOAD - SUPABASE STORAGE
# ============================================================

@router.post("/gallery/upload/image")
async def upload_gallery_image(
    title: str,
    category: str,
    description: str = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload gallery image to Supabase Storage"""

    try:
        file_extension = file.filename.split(".")[-1]

        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        storage_path = f"gallery/images/{unique_filename}"

        content = await file.read()

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            storage_path,
            content,
            {
                "content-type": file.content_type or "application/octet-stream",
                "upsert": "false"
            }
        )

        image_url = supabase.storage.from_(
            SUPABASE_BUCKET
        ).get_public_url(storage_path)

        db_image = GalleryImage(
            title=title,
            description=description,
            image_url=image_url,
            category=category,
            is_active=True
        )

        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return {
            "id": db_image.id,
            "title": db_image.title,
            "description": db_image.description,
            "image_url": db_image.image_url,
            "category": db_image.category,
            "is_active": db_image.is_active,
            "created_at": db_image.created_at,
            "message": "Image uploaded successfully"
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Image upload failed: {str(e)}"
        )


# ============================================================
# GALLERY VIDEO UPLOAD - SUPABASE STORAGE
# ============================================================

@router.post("/gallery/upload/video")
async def upload_gallery_video(
    title: str,
    category: str,
    description: str = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload gallery video to Supabase Storage"""

    try:
        file_extension = file.filename.split(".")[-1]

        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        storage_path = f"gallery/videos/{unique_filename}"

        content = await file.read()

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            storage_path,
            content,
            {
                "content-type": file.content_type or "application/octet-stream",
                "upsert": "false"
            }
        )

        video_url = supabase.storage.from_(
            SUPABASE_BUCKET
        ).get_public_url(storage_path)

        db_video = GalleryclassVedio(
            title=title,
            description=description,
            image_url=video_url,
            category=category,
            is_active=True
        )

        db.add(db_video)
        db.commit()
        db.refresh(db_video)

        return {
            "id": db_video.id,
            "title": db_video.title,
            "description": db_video.description,
            "video_url": db_video.image_url,
            "category": db_video.category,
            "is_active": db_video.is_active,
            "created_at": db_video.created_at,
            "message": "Video uploaded successfully"
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Video upload failed: {str(e)}"
        )


# ============================================================
# TEAM MEMBER UPLOAD - SUPABASE STORAGE
# ============================================================

@router.post("/team/upload")
async def create_team_member_with_image(
    name: str,
    role: str,
    bio: str = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Create team member with image upload to Supabase Storage"""

    try:
        file_extension = file.filename.split(".")[-1]

        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        storage_path = f"teachers/{unique_filename}"

        content = await file.read()

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            storage_path,
            content,
            {
                "content-type": file.content_type or "application/octet-stream",
                "upsert": "false"
            }
        )

        image_url = supabase.storage.from_(
            SUPABASE_BUCKET
        ).get_public_url(storage_path)

        db_member = TeamMember(
            name=name,
            role=role,
            bio=bio,
            image_url=image_url,
            is_active=True
        )

        db.add(db_member)
        db.commit()
        db.refresh(db_member)

        return {
            "id": db_member.id,
            "name": db_member.name,
            "role": db_member.role,
            "bio": db_member.bio,
            "image_url": db_member.image_url,
            "is_active": db_member.is_active,
            "created_at": db_member.created_at,
            "message": "Team member created successfully"
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Team member upload failed: {str(e)}"
        )


# ============================================================
# TEAM MEMBER CRUD
# ============================================================

@router.post("/team")
def create_team_member(
    member_data: dict,
    db: Session = Depends(get_db)
):
    """Create team member without image"""

    member = TeamMember(**member_data)

    db.add(member)
    db.commit()
    db.refresh(member)

    return {
        "id": member.id,
        "name": member.name,
        "role": member.role,
        "bio": member.bio,
        "image_url": member.image_url,
        "is_active": member.is_active,
        "created_at": member.created_at,
        "message": "Team member created successfully"
    }


@router.get("/team", response_model=List[dict])
def get_all_team_members(db: Session = Depends(get_db)):
    """Get all active team members"""

    team = db.query(TeamMember).filter(
        TeamMember.is_active == True
    ).all()

    return [
        {
            "id": t.id,
            "name": t.name,
            "role": t.role,
            "bio": t.bio,
            "image_url": t.image_url,
            "is_active": t.is_active,
            "created_at": t.created_at
        }
        for t in team
    ]


@router.get("/team/{team_id}", response_model=dict)
def get_team_member_by_id(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get team member by ID"""

    member = db.query(TeamMember).filter(
        TeamMember.id == team_id,
        TeamMember.is_active == True
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Team member not found"
        )

    return {
        "id": member.id,
        "name": member.name,
        "role": member.role,
        "bio": member.bio,
        "image_url": member.image_url,
        "is_active": member.is_active,
        "created_at": member.created_at
    }


@router.put("/team/{team_id}")
def update_team_member(
    team_id: int,
    member_data: dict,
    db: Session = Depends(get_db)
):
    """Update team member"""

    member = db.query(TeamMember).filter(
        TeamMember.id == team_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Team member not found"
        )

    for key, value in member_data.items():
        if hasattr(member, key):
            setattr(member, key, value)

    db.commit()
    db.refresh(member)

    return {
        "id": member.id,
        "name": member.name,
        "role": member.role,
        "bio": member.bio,
        "image_url": member.image_url,
        "is_active": member.is_active,
        "created_at": member.created_at,
        "message": "Team member updated successfully"
    }


@router.delete("/team/{team_id}")
def delete_team_member(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Delete team member"""

    member = db.query(TeamMember).filter(
        TeamMember.id == team_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Team member not found"
        )

    # Delete image from Supabase Storage
    if member.image_url and "/storage/v1/object/public/academy-media/" in member.image_url:

        storage_path = member.image_url.split(
            "/storage/v1/object/public/academy-media/",
            1
        )[1]

        try:
            supabase.storage.from_(SUPABASE_BUCKET).remove(
                [storage_path]
            )
        except Exception as e:
            print(f"Supabase team image delete failed: {e}")

    # Delete old local file if old URL exists
    elif member.image_url and member.image_url.startswith("/app/uploads/"):

        file_path = member.image_url.replace(
            "/app/uploads/",
            "app/uploads/"
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(member)
    db.commit()

    return {
        "message": "Team member deleted permanently"
    }


# ============================================================
# GALLERY IMAGES
# ============================================================

@router.get("/gallery/images", response_model=List[dict])
def get_gallery_images(db: Session = Depends(get_db)):
    """Get all active gallery images"""

    images = db.query(GalleryImage).filter(
        GalleryImage.is_active == True
    ).all()

    return [
        {
            "id": img.id,
            "title": img.title,
            "description": img.description,
            "image_url": img.image_url,
            "category": img.category,
            "is_active": img.is_active,
            "created_at": img.created_at
        }
        for img in images
    ]


@router.put("/gallery/images/{image_id}")
def update_gallery_image(
    image_id: int,
    image_data: dict,
    db: Session = Depends(get_db)
):
    """Update gallery image"""

    image = db.query(GalleryImage).filter(
        GalleryImage.id == image_id
    ).first()

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Gallery image not found"
        )

    for key, value in image_data.items():
        if hasattr(image, key):
            setattr(image, key, value)

    db.commit()
    db.refresh(image)

    return {
        "id": image.id,
        "title": image.title,
        "description": image.description,
        "image_url": image.image_url,
        "category": image.category,
        "is_active": image.is_active,
        "created_at": image.created_at,
        "message": "Gallery image updated successfully"
    }


@router.delete("/gallery/images/{image_id}")
def delete_gallery_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    """Delete gallery image"""

    image = db.query(GalleryImage).filter(
        GalleryImage.id == image_id
    ).first()

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Gallery image not found"
        )

    # Delete image from Supabase Storage
    if image.image_url and "/storage/v1/object/public/academy-media/" in image.image_url:

        storage_path = image.image_url.split(
            "/storage/v1/object/public/academy-media/",
            1
        )[1]

        try:
            supabase.storage.from_(SUPABASE_BUCKET).remove(
                [storage_path]
            )
        except Exception as e:
            print(f"Supabase gallery image delete failed: {e}")

    # Delete old local file if old URL exists
    elif image.image_url and image.image_url.startswith("/app/uploads/"):

        file_path = image.image_url.replace(
            "/app/uploads/",
            "app/uploads/"
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(image)
    db.commit()

    return {
        "message": "Gallery image deleted permanently"
    }


# ============================================================
# GALLERY VIDEOS
# ============================================================

@router.get("/gallery/videos", response_model=List[dict])
def get_gallery_videos(db: Session = Depends(get_db)):
    """Get all active gallery videos"""

    videos = db.query(GalleryclassVedio).filter(
        GalleryclassVedio.is_active == True
    ).all()

    return [
        {
            "id": vid.id,
            "title": vid.title,
            "description": vid.description,
            "video_url": vid.image_url,
            "category": vid.category,
            "is_active": vid.is_active,
            "created_at": vid.created_at
        }
        for vid in videos
    ]


@router.put("/gallery/videos/{video_id}")
def update_gallery_video(
    video_id: int,
    video_data: dict,
    db: Session = Depends(get_db)
):
    """Update gallery video"""

    video = db.query(GalleryclassVedio).filter(
        GalleryclassVedio.id == video_id
    ).first()

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Gallery video not found"
        )

    for key, value in video_data.items():
        if hasattr(video, key):
            setattr(video, key, value)

    db.commit()
    db.refresh(video)

    return {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "video_url": video.image_url,
        "category": video.category,
        "is_active": video.is_active,
        "created_at": video.created_at,
        "message": "Gallery video updated successfully"
    }


@router.delete("/gallery/videos/{video_id}")
def delete_gallery_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """Delete gallery video"""

    video = db.query(GalleryclassVedio).filter(
        GalleryclassVedio.id == video_id
    ).first()

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Gallery video not found"
        )

    # Delete video from Supabase Storage
    if video.image_url and "/storage/v1/object/public/academy-media/" in video.image_url:

        storage_path = video.image_url.split(
            "/storage/v1/object/public/academy-media/",
            1
        )[1]

        try:
            supabase.storage.from_(SUPABASE_BUCKET).remove(
                [storage_path]
            )
        except Exception as e:
            print(f"Supabase gallery video delete failed: {e}")

    # Delete old local file if old URL exists
    elif video.image_url and video.image_url.startswith("/app/uploads/"):

        file_path = video.image_url.replace(
            "/app/uploads/",
            "app/uploads/"
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(video)
    db.commit()

    return {
        "message": "Gallery video deleted permanently"
    }


# ============================================================
# GET ALL GALLERY ITEMS
# ============================================================

@router.get("/gallery", response_model=List[dict])
def get_gallery_all(db: Session = Depends(get_db)):
    """Get all active gallery items"""

    images = db.query(GalleryImage).filter(
        GalleryImage.is_active == True
    ).all()

    videos = db.query(GalleryclassVedio).filter(
        GalleryclassVedio.is_active == True
    ).all()

    result = []

    for img in images:
        result.append({
            "id": img.id,
            "title": img.title,
            "description": img.description,
            "url": img.image_url,
            "category": img.category,
            "type": "image",
            "is_active": img.is_active,
            "created_at": img.created_at
        })

    for vid in videos:
        result.append({
            "id": vid.id,
            "title": vid.title,
            "description": vid.description,
            "url": vid.image_url,
            "category": vid.category,
            "type": "video",
            "is_active": vid.is_active,
            "created_at": vid.created_at
        })

    return result


# ============================================================
# GET IMAGE BY ID
# ============================================================

@router.get("/gallery/images/{image_id}", response_model=dict)
def get_gallery_image_by_id(
    image_id: int,
    db: Session = Depends(get_db)
):
    """Get gallery image by ID"""

    image = db.query(GalleryImage).filter(
        GalleryImage.id == image_id,
        GalleryImage.is_active == True
    ).first()

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Gallery image not found"
        )

    return {
        "id": image.id,
        "title": image.title,
        "description": image.description,
        "image_url": image.image_url,
        "category": image.category,
        "is_active": image.is_active,
        "created_at": image.created_at
    }


# ============================================================
# GET VIDEO BY ID
# ============================================================

@router.get("/gallery/videos/{video_id}", response_model=dict)
def get_gallery_video_by_id(
    video_id: int,
    db: Session = Depends(get_db)
):
    """Get gallery video by ID"""

    video = db.query(GalleryclassVedio).filter(
        GalleryclassVedio.id == video_id,
        GalleryclassVedio.is_active == True
    ).first()

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Gallery video not found"
        )

    return {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "video_url": video.image_url,
        "category": video.category,
        "is_active": video.is_active,
        "created_at": video.created_at
    }
