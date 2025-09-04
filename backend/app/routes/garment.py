from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.database import get_db
from app.models.user import User
from app.models.garment import Garment, GeneratedImage, GarmentTypeEnum
from app.models.mannequin import UserMannequin
from app.schemas.garment import (
    GarmentCreate, 
    GarmentResponse, 
    TryOnRequest,
    GeneratedImageResponse
)
from app.routes.auth import get_current_user
from app.services.generation import image_generator

router = APIRouter(prefix="/garment", tags=["garment"])

@router.post("/create", response_model=GarmentResponse)
def create_garment(
    garment: GarmentCreate,
    db: Session = Depends(get_db)
):
    """Crea una nova peça de roba al catàleg"""
    
    db_garment = Garment(**garment.dict())
    db.add(db_garment)
    db.commit()
    db.refresh(db_garment)
    
    return db_garment

@router.get("/catalog", response_model=List[GarmentResponse])
def get_garment_catalog(
    type: Optional[GarmentTypeEnum] = Query(None),
    color: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Obté el catàleg de peces de roba amb filtres opcionals"""
    
    query = db.query(Garment)
    
    if type:
        query = query.filter(Garment.type == type)
    if color:
        query = query.filter(Garment.color.ilike(f"%{color}%"))
    if size:
        query = query.filter(Garment.size == size)
    if brand:
        query = query.filter(Garment.brand.ilike(f"%{brand}%"))
    
    garments = query.offset(offset).limit(limit).all()
    return garments

@router.get("/{garment_id}", response_model=GarmentResponse)
def get_garment_by_id(
    garment_id: int,
    db: Session = Depends(get_db)
):
    """Obté una peça específica per ID"""
    
    garment = db.query(Garment).filter(Garment.id == garment_id).first()
    
    if not garment:
        raise HTTPException(
            status_code=404,
            detail="Garment not found"
        )
    
    return garment

@router.post("/try-on", response_model=GeneratedImageResponse)
async def try_on_garment(
    try_on_request: TryOnRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Prova una peça de roba sobre un maniquí de l'usuari"""
    
    # Verificar que el maniquí pertany a l'usuari
    mannequin = db.query(UserMannequin).filter(
        UserMannequin.id == try_on_request.mannequin_id,
        UserMannequin.user_id == current_user.id
    ).first()
    
    if not mannequin:
        raise HTTPException(
            status_code=404,
            detail="Mannequin not found or doesn't belong to user"
        )
    
    # Verificar que la peça existeix
    garment = db.query(Garment).filter(
        Garment.id == try_on_request.garment_id
    ).first()
    
    if not garment:
        raise HTTPException(
            status_code=404,
            detail="Garment not found"
        )
    
    # Generar imatge del maniquí vestit
    try:
        image_path = await image_generator.generate_dressed_mannequin(
            mannequin, garment, try_on_request.additional_prompt
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating image: {str(e)}"
        )
    
    # Construir el prompt utilitzat per debug
    measurements = {
        'height': mannequin.height,
        'chest': mannequin.chest,
        'waist': mannequin.waist,
        'hips': mannequin.hips,
        'shoulders': mannequin.shoulders
    }
    
    mannequin_prompt = image_generator._build_mannequin_prompt(
        measurements, current_user.gender
    )
    garment_prompt = image_generator._build_garment_prompt(
        mannequin_prompt, garment, try_on_request.additional_prompt
    )
    
    # Guardar el resultat a la base de dades
    generated_image = GeneratedImage(
        user_id=current_user.id,
        mannequin_id=mannequin.id,
        garment_id=garment.id,
        image_path=image_path,
        prompt_used=garment_prompt
    )
    
    db.add(generated_image)
    db.commit()
    db.refresh(generated_image)
    
    return generated_image

@router.get("/images/history", response_model=List[GeneratedImageResponse])
def get_user_generated_images(
    current_user: User = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Obté l'historial d'imatges generades de l'usuari"""
    
    images = db.query(GeneratedImage).filter(
        GeneratedImage.user_id == current_user.id
    ).order_by(GeneratedImage.created_at.desc()).offset(offset).limit(limit).all()
    
    return images

@router.get("/images/{image_id}", response_model=GeneratedImageResponse)
def get_generated_image_by_id(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obté una imatge generada específica"""
    
    image = db.query(GeneratedImage).filter(
        GeneratedImage.id == image_id,
        GeneratedImage.user_id == current_user.id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=404,
            detail="Generated image not found"
        )
    
    return image

@router.delete("/images/{image_id}")
def delete_generated_image(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina una imatge generada"""
    
    image = db.query(GeneratedImage).filter(
        GeneratedImage.id == image_id,
        GeneratedImage.user_id == current_user.id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=404,
            detail="Generated image not found"
        )
    
    # Eliminar fitxer físic si existeix
    if image.image_path and os.path.exists(image.image_path):
        os.remove(image.image_path)
        
        # També eliminar el fitxer de prompt si existeix
        prompt_file = image.image_path.replace('.png', '_prompt.txt')
        if os.path.exists(prompt_file):
            os.remove(prompt_file)
    
    db.delete(image)
    db.commit()
    
    return {"message": "Generated image deleted successfully"}

@router.post("/batch-create", response_model=List[GarmentResponse])
def create_garments_batch(
    garments: List[GarmentCreate],
    db: Session = Depends(get_db)
):
    """Crea múltiples peces de roba en lot"""
    
    if len(garments) > 50:
        raise HTTPException(
            status_code=400,
            detail="Maximum 50 garments per batch"
        )
    
    db_garments = []
    for garment_data in garments:
        db_garment = Garment(**garment_data.dict())
        db.add(db_garment)
        db_garments.append(db_garment)
    
    db.commit()
    
    for garment in db_garments:
        db.refresh(garment)
    
    return db_garments

@router.get("/types/available")
def get_available_garment_types():
    """Retorna els tipus de peces disponibles"""
    
    return {
        "types": [type.value for type in GarmentTypeEnum],
        "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "fits": ["slim", "regular", "loose", "oversized"]
    }