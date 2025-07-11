
# API de Mapa Astral com FastAPI + Flatlib

## 📦 Requisitos

- Python 3.9+
- Conta gratuita no https://opencagedata.com/

## 🚀 Como usar

### 1. Clone e instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Adicione sua chave da OpenCage no main.py

Substitua `"SUA_CHAVE_API_DO_OPENCAGE"` pela sua chave real.

### 3. Execute localmente

```bash
uvicorn main:app --reload
```

Acesse em: http://localhost:8000/docs

### 4. Deploy no Render ou Heroku

Inclui `Procfile` pronto para deploy automático.

---

### 🔗 Endpoint

`POST /mapa-astral`

**Body JSON:**
```json
{
  "nome": "Joana",
  "data_nascimento": "1990-08-15",
  "hora_nascimento": "14:35",
  "cidade_nascimento": "São Paulo, Brasil"
}
```

**Resposta JSON:**
```json
{
  "nome": "Joana",
  "signo_solar": "Leão",
  "signo_lunar": "Peixes",
  "ascendente": "Sagitário",
  "planetas": {
    "SUN": "Leão - 22.55°",
    "MOON": "Peixes - 15.01°",
    ...
  }
}
```
