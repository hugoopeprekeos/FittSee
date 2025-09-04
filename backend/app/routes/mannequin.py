from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.mannequin import BaseMannequin, UserMannequin
from app.schemas.mannequin import (
    MannequinMatch, 
    BaseMannequinResponse, 
    MannequinMatchResponse,
    MannequinCustomize,
    UserMannequinResponse
)
from app.routes.auth import get_current_user
from app.services.matching import mannequin_matcher
from app.services.generation import image_generator

router = APIRouter(prefix="/mannequin", tags=["mannequin"])

@router.post("/match", response_model=MannequinMatchResponse)
async def find_mannequin_matches(
    match_request: MannequinMatch,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Troba els maniquins més semblants a les mesures de l'usuari"""
    
    user_measurements = {
        'height': match_request.height,
        'chest': match_request.chest,
        'waist': match_request.waist,
        'hips': match_request.hips,
        'shoulders': match_request.shoulders or 0
    }
    
    # Trobar els 3 millors matches
    matches = mannequin_matcher.find_best_matches(
        db, user_measurements, match_request.gender, top_k=3
    )
    
    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No mannequins found for the specified gender"
        )
    
    # Convertir a response format
    match_responses = []
    for mannequin, similarity in matches:
        response = BaseMannequinResponse.from_orm(mannequin)
        response.similarity_score = similarity
        match_responses.append(response)
    
    return MannequinMatchResponse(
        matches=match_responses,
        best_match=match_responses[0]
    )

@router.post("/generate", response_model=UserMannequinResponse)
async def generate_mannequin_from_match(
    mannequin_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Genera un maniquí d'usuari basant-se en un match de la base de dades"""
    
    # Verificar que el maniquí base existeix
    base_mannequin = db.query(BaseMannequin).filter(
        BaseMannequin.id == mannequin_id
    ).first()
    
    if not base_mannequin:
        raise HTTPException(
            status_code=404,
            detail="Base mannequin not found"
        )
    
    # Verificar que l'usuari té mesures configurades
    if not all([current_user.height, current_user.chest, current_user.waist, current_user.hips]):
        raise HTTPException(
            status_code=400,
            detail="User measurements are incomplete. Please update your profile first."
        )
    
    # Crear maniquí d'usuari
    user_mannequin = UserMannequin(
        user_id=current_user.id,
        base_mannequin_id=base_mannequin.id,
        height=current_user.height,
        chest=current_user.chest,
        waist=current_user.waist,
        hips=current_user.hips,
        shoulders=current_user.shoulders or base_mannequin.shoulders,
        is_custom=0
    )
    
    db.add(user_mannequin)
    db.commit()
    db.refresh(user_mannequin)
    
    # Generar imatge del maniquí
    measurements = {
        'height': user_mannequin.height,
        'chest': user_mannequin.chest,
        'waist': user_mannequin.waist,
        'hips': user_mannequin.hips,
        'shoulders': user_mannequin.shoulders
    }
    
    image_path = await image_generator.generate_mannequin_image(
        measurements, current_user.gender
    )
    
    # Actualitzar amb el path de la imatge
    user_mannequin.image_path = image_path
    db.commit()
    db.refresh(user_mannequin)
    
    return user_mannequin

@router.post("/customize", response_model=UserMannequinResponse)
async def customize_mannequin(
    customize_request: MannequinCustomize,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea un maniquí personalitzat amb mesures específiques"""
    
    # Crear maniquí customitzat
    user_mannequin = UserMannequin(
        user_id=current_user.id,
        base_mannequin_id=customize_request.base_mannequin_id,
        height=customize_request.height,
        chest=customize_request.chest,
        waist=customize_request.waist,
        hips=customize_request.hips,
        shoulders=customize_request.shoulders,
        is_custom=1
    )
    
    db.add(user_mannequin)
    db.commit()
    db.refresh(user_mannequin)
    
    # Generar imatge personalitzada
    measurements = {
        'height': customize_request.height,
        'chest': customize_request.chest,
        'waist': customize_request.waist,
        'hips': customize_request.hips,
        'shoulders': customize_request.shoulders
    }
    
    image_path = await image_generator.generate_mannequin_image(
        measurements, current_user.gender
    )
    
    # Actualitzar amb el path de la imatge
    user_mannequin.image_path = image_path
    db.commit()
    db.refresh(user_mannequin)
    
    return user_mannequin

@router.get("/my-mannequins", response_model=List[UserMannequinResponse])
def get_user_mannequins(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obté tots els maniquins de l'usuari"""
    
    mannequins = db.query(UserMannequin).filter(
        UserMannequin.user_id == current_user.id
    ).all()
    
    return mannequins

@router.get("/{mannequin_id}", response_model=UserMannequinResponse)
def get_mannequin_by_id(
    mannequin_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obté un maniquí específic de l'usuari"""
    
    mannequin = db.query(UserMannequin).filter(
        UserMannequin.id == mannequin_id,
        UserMannequin.user_id == current_user.id
    ).first()
    
    if not mannequin:
        raise HTTPException(
            status_code=404,
            detail="Mannequin not found"
        )
    
    return mannequin

@router.delete("/{mannequin_id}")
def delete_mannequin(
    mannequin_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina un maniquí de l'usuari"""
    
    mannequin = db.query(UserMannequin).filter(
        UserMannequin.id == mannequin_id,
        UserMannequin.user_id == current_user.id
    ).first()
    
    if not mannequin:
        raise HTTPException(
            status_code=404,
            detail="Mannequin not found"
        )
    
    # Eliminar imatge si existeix
    if mannequin.image_path and os.path.exists(mannequin.image_path):
        os.remove(mannequin.image_path)
    
    db.delete(mannequin)
    db.commit()
    
    return {"message": "Mannequin deleted successfully"}

@router.get("/base/all", response_model=List[BaseMannequinResponse])
def get_all_base_mannequins(
    gender: str = None,
    db: Session = Depends(get_db)
):
    """Obté tots els maniquins base disponibles"""
    
    query = db.query(BaseMannequin)
    
    if gender:
        query = query.filter(BaseMannequin.gender == gender)
    
    mannequins = query.all()
    return mannequins