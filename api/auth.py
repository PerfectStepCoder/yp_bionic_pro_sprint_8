from fastapi import Request, HTTPException
from jose import jwt, jwk
import requests

KEYCLOAK_URL = "http://keycloak:8080"
REALM = "reports-realm"
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

# Получаем JWK-и один раз при старте
jwks = requests.get(JWKS_URL).json()

def get_public_key(token: str):
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    if not kid:
        raise HTTPException(status_code=401, detail="Missing kid in token header")

    for key_dict in jwks["keys"]:
        if key_dict["kid"] == kid:
            return jwk.construct(key_dict)  # ← исправление здесь

    raise HTTPException(status_code=401, detail="Public key not found")

def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = auth.split(" ")[1]
    public_key = get_public_key(token)

    try:
        payload = jwt.decode(
            token,
            key=public_key,
            algorithms=["RS256"],
            audience="reports-api"  # clientId из Keycloak
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Invalid claims")
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalid")

def has_role(user_payload, role: str) -> bool:
    roles = user_payload.get("realm_access", {}).get("roles", [])
    return role in roles
