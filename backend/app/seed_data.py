"""
Script per omplir la base de dades amb dades de prova
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, create_tables
from app.models.user import User, GenderEnum
from app.models.mannequin import BaseMannequin
from app.models.garment import Garment, GarmentTypeEnum, FitTypeEnum, SizeEnum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_base_mannequins(db: Session):
    """Crea maniquins base per matching"""
    
    base_mannequins = [
        # Maniquins femenins
        {
            "name": "Emma - Petite Athletic",
            "image_path": "static/images/base_emma.png",
            "gender": GenderEnum.female,
            "height": 158.0,
            "chest": 86.0,
            "waist": 66.0,
            "hips": 92.0,
            "shoulders": 38.0
        },
        {
            "name": "Sofia - Average Hourglass",
            "image_path": "static/images/base_sofia.png", 
            "gender": GenderEnum.female,
            "height": 168.0,
            "chest": 94.0,
            "waist": 72.0,
            "hips": 98.0,
            "shoulders": 40.0
        },
        {
            "name": "Clara - Tall Slim",
            "image_path": "static/images/base_clara.png",
            "gender": GenderEnum.female,
            "height": 178.0,
            "chest": 88.0,
            "waist": 68.0,
            "hips": 94.0,
            "shoulders": 42.0
        },
        {
            "name": "Maria - Curvy Plus",
            "image_path": "static/images/base_maria.png",
            "gender": GenderEnum.female,
            "height": 165.0,
            "chest": 104.0,
            "waist": 82.0,
            "hips": 108.0,
            "shoulders": 44.0
        },
        
        # Maniquins masculins
        {
            "name": "Alex - Slim Build",
            "image_path": "static/images/base_alex.png",
            "gender": GenderEnum.male,
            "height": 175.0,
            "chest": 92.0,
            "waist": 78.0,
            "hips": 88.0,
            "shoulders": 46.0
        },
        {
            "name": "Marc - Athletic Average",
            "image_path": "static/images/base_marc.png",
            "gender": GenderEnum.male,
            "height": 180.0,
            "chest": 102.0,
            "waist": 84.0,
            "hips": 96.0,
            "shoulders": 50.0
        },
        {
            "name": "David - Tall Athletic",
            "image_path": "static/images/base_david.png",
            "gender": GenderEnum.male,
            "height": 188.0,
            "chest": 108.0,
            "waist": 88.0,
            "hips": 98.0,
            "shoulders": 52.0
        },
        {
            "name": "Pau - Stocky Build",
            "image_path": "static/images/base_pau.png",
            "gender": GenderEnum.male,
            "height": 172.0,
            "chest": 106.0,
            "waist": 92.0,
            "hips": 102.0,
            "shoulders": 48.0
        }
    ]
    
    for mannequin_data in base_mannequins:
        existing = db.query(BaseMannequin).filter(
            BaseMannequin.name == mannequin_data["name"]
        ).first()
        
        if not existing:
            mannequin = BaseMannequin(**mannequin_data)
            db.add(mannequin)
    
    db.commit()
    print("✅ Base mannequins created successfully!")

def seed_garments(db: Session):
    """Crea peces de roba de prova"""
    
    garments = [
        # Samarretes
        {
            "name": "Basic White T-Shirt",
            "type": GarmentTypeEnum.tshirt,
            "brand": "BasicWear",
            "color": "white",
            "size": SizeEnum.m,
            "fit": FitTypeEnum.regular,
            "chest_fit": 100.0,
            "length": 68.0
        },
        {
            "name": "Slim Black T-Shirt",
            "type": GarmentTypeEnum.tshirt,
            "brand": "SlimFit",
            "color": "black",
            "size": SizeEnum.m,
            "fit": FitTypeEnum.slim,
            "chest_fit": 96.0,
            "length": 66.0
        },
        {
            "name": "Oversized Red T-Shirt",
            "type": GarmentTypeEnum.tshirt,
            "brand": "StreetStyle",
            "color": "red",
            "size": SizeEnum.l,
            "fit": FitTypeEnum.oversized,
            "chest_fit": 110.0,
            "length": 72.0
        },
        
        # Pantalons
        {
            "name": "Classic Blue Jeans",
            "type": GarmentTypeEnum.pants,
            "brand": "DenimCo",
            "color": "blue",
            "size": SizeEnum.m,
            "fit": FitTypeEnum.regular,
            "waist_fit": 84.0,
            "hip_fit": 98.0,
            "length": 108.0
        },
        {
            "name": "Slim Black Jeans",
            "type": GarmentTypeEnum.pants,
            "brand": "SlimFit",
            "color": "black",
            "size": SizeEnum.m,
            "fit": FitTypeEnum.slim,
            "waist_fit": 80.0,
            "hip_fit": 94.0,
            "length": 106.0
        },
        {
            "name": "Loose Cargo Pants",
            "type": GarmentTypeEnum.pants,
            "brand": "UtilityWear",
            "color": "khaki",
            "size": SizeEnum.l,
            "fit": FitTypeEnum.loose,
            "waist_fit": 90.0,
            "hip_fit": 105.0,
            "length": 110.0
        },
        
        # Vestits
        {
            "name": "Summer Floral Dress",
            "type": GarmentTypeEnum.dress,
            "brand": "FloralStyle",
            "color": "floral",
            "size": SizeEnum.m,
            "fit": FitTypeEnum.regular,
            "chest_fit": 94.0,
            "waist_fit": 76.0,
            "hip_fit": 98.0,
            "length": 95.0
        },
        {
            "name": "Little Black Dress",
            "type": GarmentTypeEnum.dress,
            "brand": "Elegant",
            "color": "black",
            "size": SizeEnum.s,
            "fit": FitTypeEnum.slim,
            "chest_fit": 88.0,
            "waist_fit": 70.0,
            "hip_fit": 92.0,
            "length": 85.0
        },
        
        # Jaquetes
        {
            "name": "Denim Jacket",
            "type": GarmentTypeEnum.jacket,
            "brand": "DenimCo",
            "color": "blue",
            "size": SizeEnum.m,
            "fit": FitTypeEnum.regular,
            "chest_fit": 104.0,
            "length": 62.0
        },
        {
            "name": "Black Leather Jacket",
            "type": GarmentTypeEnum.jacket,
            "brand": "RockStyle",
            "color": "black",
            "size": SizeEnum.m,
            "fit": FitTypeEnum.slim,
            "chest_fit": 98.0,
            "length": 58.0
        },
        
        # Jerseis
        {
            "name": "Cozy Wool Sweater",
            "type": GarmentTypeEnum.sweater,
            "brand": "WarmWear",
            "color": "gray",
            "size": SizeEnum.m,
            "fit": FitTypeEnum.regular,
            "chest_fit": 102.0,
            "length": 65.0
        },
        {
            "name": "Chunky Knit Sweater",
            "type": GarmentTypeEnum.sweater,
            "brand": "CozyKnits",
            "color": "cream",
            "size": SizeEnum.l,
            "fit": FitTypeEnum.oversized,
            "chest_fit": 115.0,
            "length": 70.0
        }
    ]
    
    for garment_data in garments:
        existing = db.query(Garment).filter(
            Garment.name == garment_data["name"]
        ).first()
        
        if not existing:
            garment = Garment(**garment_data)
            db.add(garment)
    
    db.commit()
    print("✅ Sample garments created successfully!")

def seed_test_users(db: Session):
    """Crea usuaris de prova"""
    
    test_users = [
        {
            "email": "emma@test.com",
            "password": "password123",
            "gender": GenderEnum.female,
            "height": 165.0,
            "chest": 90.0,
            "waist": 70.0,
            "hips": 95.0,
            "shoulders": 39.0
        },
        {
            "email": "marc@test.com", 
            "password": "password123",
            "gender": GenderEnum.male,
            "height": 178.0,
            "chest": 98.0,
            "waist": 82.0,
            "hips": 94.0,
            "shoulders": 48.0
        }
    ]
    
    for user_data in test_users:
        existing_user = db.query(User).filter(
            User.email == user_data["email"]
        ).first()
        
        if not existing_user:
            user_dict = user_data.copy()
            password = user_dict.pop("password")
            user_dict["hashed_password"] = get_password_hash(password)
            
            user = User(**user_dict)
            db.add(user)
    
    db.commit()
    print("✅ Test users created successfully!")

def main():
    """Executar el seed complet"""
    print("🌱 Starting database seeding...")
    
    # Crear taules si no existeixen
    create_tables()
    
    # Crear sessió de base de dades
    db = SessionLocal()
    
    try:
        # Executar seeds
        seed_base_mannequins(db)
        seed_garments(db)
        seed_test_users(db)
        
        print("\n🎉 Database seeding completed successfully!")
        print("\n📋 Test credentials:")
        print("   • emma@test.com / password123")
        print("   • marc@test.com / password123")
        print("\n🚀 You can now start the API with: uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    main()