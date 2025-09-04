import os
import json
import uuid
import requests
from typing import Dict, Any, Optional
from PIL import Image
import aiofiles
from app.models.mannequin import UserMannequin
from app.models.garment import Garment
from app.models.user import GenderEnum

class ImageGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")  # O el servei que triïs
        self.base_url = "https://api.openai.com/v1/images/generations"
        self.static_dir = "static/images"
        
        # Crear directori si no existeix
        os.makedirs(self.static_dir, exist_ok=True)
    
    def _build_mannequin_prompt(self, measurements: Dict[str, Any], gender: GenderEnum) -> str:
        """
        Construeix el prompt per generar el maniquí
        """
        gender_str = "male" if gender == GenderEnum.male else "female"
        
        # Determinar tipus de cos basant-se en mesures
        height = measurements.get('height', 170)
        chest = measurements.get('chest', 90)
        waist = measurements.get('waist', 80)
        hips = measurements.get('hips', 95)
        
        # Calcular proporcions
        waist_hip_ratio = waist / hips if hips > 0 else 0.8
        chest_waist_ratio = chest / waist if waist > 0 else 1.1
        
        # Descriptors de forma corporal
        body_descriptors = []
        if gender == GenderEnum.female:
            if waist_hip_ratio < 0.8:
                body_descriptors.append("hourglass figure")
            elif waist_hip_ratio > 0.9:
                body_descriptors.append("straight body type")
            else:
                body_descriptors.append("pear-shaped")
        else:
            if chest_waist_ratio > 1.2:
                body_descriptors.append("athletic build")
            elif chest_waist_ratio < 1.05:
                body_descriptors.append("slim build")
            else:
                body_descriptors.append("average build")
        
        if height > 180:
            body_descriptors.append("tall")
        elif height < 160:
            body_descriptors.append("petite")
        
        body_desc = ", ".join(body_descriptors)
        
        prompt = f"""
        Create a realistic 3D mannequin of a {gender_str} person with {body_desc}.
        Height: {height}cm, Chest: {chest}cm, Waist: {waist}cm, Hips: {hips}cm.
        The mannequin should be standing straight, facing forward, arms slightly away from body.
        Clean white background, professional lighting, photorealistic rendering.
        No clothing, neutral skin tone, suitable for virtual try-on applications.
        """
        
        return prompt.strip()
    
    def _build_garment_prompt(self, mannequin_prompt: str, garment: Garment, 
                            additional_prompt: Optional[str] = None) -> str:
        """
        Construeix el prompt per vestir el maniquí
        """
        garment_desc = f"{garment.color} {garment.type.value}"
        
        if garment.fit:
            garment_desc += f" with {garment.fit.value} fit"
        
        if garment.brand:
            garment_desc += f" ({garment.brand} style)"
        
        base_prompt = f"""
        Take the mannequin from the previous image and dress it with a {garment_desc}.
        The clothing should fit naturally on the mannequin's body proportions.
        Size: {garment.size.value}. Maintain the same pose and background.
        Photorealistic rendering with proper fabric textures and shadows.
        """
        
        if additional_prompt:
            base_prompt += f"\nAdditional details: {additional_prompt}"
        
        return base_prompt.strip()
    
    async def generate_mannequin_image(self, measurements: Dict[str, Any], 
                                     gender: GenderEnum) -> str:
        """
        Genera imatge del maniquí basat en mesures
        Retorna el path de la imatge generada
        """
        prompt = self._build_mannequin_prompt(measurements, gender)
        
        # Per MVP, simulem la generació guardant el prompt
        # En producció, aquí faries la crida real a l'API d'IA
        return await self._mock_image_generation(prompt, "mannequin")
    
    async def generate_dressed_mannequin(self, mannequin: UserMannequin, 
                                       garment: Garment,
                                       additional_prompt: Optional[str] = None) -> str:
        """
        Genera imatge del maniquí vestit amb la peça
        """
        # Primer necessitem el prompt del maniquí base
        measurements = {
            'height': mannequin.height,
            'chest': mannequin.chest,
            'waist': mannequin.waist,
            'hips': mannequin.hips,
            'shoulders': mannequin.shoulders
        }
        
        mannequin_prompt = self._build_mannequin_prompt(measurements, 
                                                       mannequin.user.gender)
        garment_prompt = self._build_garment_prompt(mannequin_prompt, garment, 
                                                  additional_prompt)
        
        # Generar imatge vestida
        return await self._mock_image_generation(garment_prompt, "dressed")
    
    async def _mock_image_generation(self, prompt: str, type_prefix: str) -> str:
        """
        Mock de generació d'imatges per MVP
        En producció, substituir per crida real a l'API
        """
        # Generar nom únic per la imatge
        unique_id = str(uuid.uuid4())
        filename = f"{type_prefix}_{unique_id}.png"
        filepath = os.path.join(self.static_dir, filename)
        
        # Crear imatge placeholder
        placeholder = Image.new('RGB', (512, 768), color='lightgray')
        placeholder.save(filepath)
        
        # Guardar prompt per debug
        prompt_file = filepath.replace('.png', '_prompt.txt')
        async with aiofiles.open(prompt_file, 'w') as f:
            await f.write(prompt)
        
        return filepath
    
    async def _call_ai_api(self, prompt: str) -> str:
        """
        Crida real a l'API d'IA (per implementar en producció)
        """
        # Exemple amb OpenAI DALL-E
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "n": 1,
            "size": "512x768",
            "response_format": "url"
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            
            # Descarregar i guardar imatge
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                unique_id = str(uuid.uuid4())
                filename = f"generated_{unique_id}.png"
                filepath = os.path.join(self.static_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_response.content)
                
                return filepath
        
        raise Exception(f"Error generating image: {response.text}")

# Instància global del generador
image_generator = ImageGenerator()