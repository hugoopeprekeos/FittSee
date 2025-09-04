import numpy as np
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.mannequin import BaseMannequin
from app.models.user import GenderEnum
from sklearn.preprocessing import StandardScaler

class MannequinMatcher:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def calculate_similarity(self, user_measurements: dict, mannequin_measurements: dict) -> float:
        """
        Calcula la similitud entre mesures d'usuari i maniquí
        Retorna un score de 0 (no semblant) a 1 (idèntic)
        """
        # Mesures clau per comparar
        measures = ['height', 'chest', 'waist', 'hips', 'shoulders']
        
        user_values = []
        mannequin_values = []
        
        for measure in measures:
            user_val = user_measurements.get(measure, 0)
            mann_val = mannequin_measurements.get(measure, 0)
            
            if user_val > 0 and mann_val > 0:  # Només si ambdues mesures existeixen
                user_values.append(user_val)
                mannequin_values.append(mann_val)
        
        if len(user_values) < 3:  # Mínim 3 mesures per comparar
            return 0.0
        
        # Calcular distància euclidiana normalitzada
        user_array = np.array(user_values)
        mann_array = np.array(mannequin_values)
        
        # Normalitzar per evitar que mesures grans dominin
        max_vals = np.maximum(user_array, mann_array)
        normalized_diff = np.abs(user_array - mann_array) / max_vals
        
        # Distància mitjana normalitzada
        avg_diff = np.mean(normalized_diff)
        
        # Convertir a similitud (1 - distància)
        similarity = max(0.0, 1.0 - avg_diff)
        
        return similarity
    
    def find_best_matches(self, db: Session, user_measurements: dict, 
                         gender: GenderEnum, top_k: int = 3) -> List[Tuple[BaseMannequin, float]]:
        """
        Troba els k maniquins més semblants a l'usuari
        """
        # Obtenir maniquins del mateix gènere
        mannequins = db.query(BaseMannequin).filter(
            BaseMannequin.gender == gender
        ).all()
        
        if not mannequins:
            return []
        
        matches = []
        
        for mannequin in mannequins:
            mann_measurements = {
                'height': mannequin.height,
                'chest': mannequin.chest,
                'waist': mannequin.waist,
                'hips': mannequin.hips,
                'shoulders': mannequin.shoulders
            }
            
            similarity = self.calculate_similarity(user_measurements, mann_measurements)
            matches.append((mannequin, similarity))
        
        # Ordenar per similitud (més alt primer)
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches[:top_k]
    
    def get_best_match(self, db: Session, user_measurements: dict, 
                      gender: GenderEnum) -> Tuple[BaseMannequin, float]:
        """
        Retorna el millor match individual
        """
        matches = self.find_best_matches(db, user_measurements, gender, top_k=1)
        
        if matches:
            return matches[0]
        else:
            return None, 0.0

# Instància global del matcher
mannequin_matcher = MannequinMatcher()