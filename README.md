# FittSee MVP - Backend API

Una aplicació per provar roba sobre maniquins personalitzats generats amb IA.

## ✨ Funcionalitats

- **Autenticació d'usuaris** amb JWT
- **Matching de maniquins** basant-se en mesures corporals
- **Generació de maniquins** personalitzats amb IA
- **Catàleg de peces de roba** amb filtres
- **Proves virtuals** de roba sobre maniquins
- **Historial d'imatges** generades per usuari

## 🚀 Instal·lació ràpida

1. **Clonar i preparar l'entorn**
```bash
git clone <repo-url>
cd fittsee-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

2. **Instal·lar dependències**
```bash
pip install -r requirements.txt
```

3. **Configurar variables d'entorn**
```bash
cp .env.example .env
# Edita .env amb les teves configuracions
```

4. **Omplir la base de dades amb dades de prova**
```bash
python seed_data.py
```

5. **Executar l'API**
```bash
uvicorn app.main:app --reload
```

L'API estarà disponible a: http://localhost:8000

## 📚 Documentació API

- **Docs interactives**: http://localhost:8000/docs
- **Schema OpenAPI**: http://localhost:8000/openapi.json

## 🧪 Usuaris de prova

Després d'executar `seed_data.py`:

| Email | Password | Gènere | Mesures |
|-------|----------|--------|---------|
| emma@test.com | password123 | Dona | 165cm, 90-70-95 |
| marc@test.com | password123 | Home | 178cm, 98-82-94 |

## 🔐 Flux d'autenticació

1. **Registre**: `POST /auth/register`
2. **Login**: `POST /auth/token`
3. **Actualitzar mesures**: `PUT /auth/me/measurements`

## 📐 Workflow principal

### 1. Trobar maniquí semblant
```bash
POST /mannequin/match
{
  "gender": "female",
  "height": 165,
  "chest": 90,
  "waist": 70,
  "hips": 95,
  "shoulders": 39
}
```

### 2. Generar maniquí personalitzat
```bash
POST /mannequin/generate
{
  "mannequin_id": 1
}
```

### 3. Personalitzar mesures (opcional)
```bash
POST /mannequin/customize
{
  "height": 167,
  "chest": 92,
  "waist": 72,
  "hips": 96,
  "shoulders": 40
}
```

### 4. Provar roba
```bash
POST /garment/try-on
{
  "mannequin_id": 1,
  "garment_id": 5,
  "additional_prompt": "casual summer look"
}
```

## 🎯 Endpoints principals

### Autenticació
- `POST /auth/register` - Registrar usuari
- `POST /auth/token` - Login i obtenir token
- `GET /auth/me` - Perfil de l'usuari
- `PUT /auth/me/measurements` - Actualitzar mesures

### Maniquins
- `POST /mannequin/match` - Trobar maniquins semblants
- `POST /mannequin/generate` - Generar maniquí d'usuari
- `POST /mannequin/customize` - Crear maniquí personalitzat
- `GET /mannequin/my-mannequins` - Llistar maniquins de l'usuari
- `GET /mannequin/base/all` - Maniquins base disponibles

### Peces de roba
- `GET /garment/catalog` - Catàleg amb filtres
- `POST /garment/try-on` - Provar peça sobre maniquí
- `GET /garment/images/history` - Historial d'imatges
- `GET /garment/types/available` - Tipus i talles disponibles

## 🧮 Algorisme de matching

El sistema utilitza **distància euclidiana normalitzada** per trobar els maniquins més semblants:

1. Compara mesures clau: alçada, pit, cintura, malucs, espatlles
2. Normalitza les diferències per evitar dominància de mesures grans
3. Calcula similitud com `1 - distància_mitjana`
4. Retorna els 3 millors matches ordenats per similitud

## 🎨 Generació d'imatges

### MVP (Mock)
- Crea imatges placeholder de 512x768px
- Guarda prompts utilitzats per debug
- Simula el workflow de generació real

### Producció (per implementar)
- Integració amb OpenAI DALL-E, Stability AI, etc.
- Prompts optimitzats per cada tipus de peça
- Post-processament d'imatges

## 📊 Models de dades

### User
- Informació bàsica + mesures corporals
- Relació amb maniquins i imatges generades

### BaseMannequin
- Maniquins pre-generats per matching
- Mesures representatives de diferents tipus de cos

### UserMannequin  
- Maniquins personalitzats per usuari
- Poden ser basats en matching o completament customitzats

### Garment
- Catàleg de peces de roba
- Mesures de fit específiques per tipus

### GeneratedImage
- Historial d'imatges generades
- Enllaç a maniquí i peça utilitzats

## 🛠️ Tecnologies

- **FastAPI** - Framework web modern i ràpid
- **SQLAlchemy** - ORM per gestió de base de dades
- **JWT** - Autenticació segura
- **Pydantic** - Validació de dades
- **scikit-learn** - Algoritmes de matching
- **Pillow** - Processament d'imatges
- **PostgreSQL/SQLite** - Base de dades

## 📁 Estructura del projecte

```
backend/
├── app/
│   ├── main.py              # Entrypoint FastAPI
│   ├── database.py          # Configuració DB
│   ├── models/              # Models SQLAlchemy
│   │   ├── user.py
│   │   ├── mannequin.py
│   │   └── garment.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── user.py
│   │   ├── mannequin.py
│   │   └── garment.py
│   ├── routes/              # Endpoints API
│   │   ├── auth.py
│   │   ├── mannequin.py
│   │   └── garment.py
│   └── services/            # Lògica de negoci
│       ├── matching.py
│       └── generation.py
├── static/images/           # Imatges generades
├── seed_data.py            # Dades de prova
├── requirements.txt        # Dependències
└── .env.example           # Variables d'entorn
```

## 🚧 Millores futures

- [ ] Integració real amb APIs d'IA
- [ ] Càrrega d'imatges de referència per peces
- [ ] Millor algoritme de matching amb ML
- [ ] Cache de resultats de generació
- [ ] Processament d'imatges en background
- [ ] Sistema de valoracions per peces
- [ ] Recomanacions personalitzades
- [ ] Suport per múltiples idiomes

## 🤝 Contribució

1. Fork del projecte
2. Crear branch per feature (`git checkout -b feature/nova-funcio`)
3. Commit dels canvis (`git commit -am 'Afegir nova funcionalitat'`)
4. Push al branch (`git push origin feature/nova-funcio`)
5. Crear Pull Request

## 📝 Llicència

Aquest projecte està sota llicència MIT. Veure `LICENSE` per més detalls.