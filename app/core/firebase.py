import firebase_admin
from firebase_admin import auth as firebase_auth, credentials

from .config import settings


def _get_firebase_credentials():
    """
    Si hay archivo de service account -> usarlo.
    Si no, usar Application Default Credentials (ADC):
        - gcloud auth application-default login
        - credenciales del entorno en GCP (Cloud Run, GCE, etc.)
    """
    if settings.firebase_credentials_file:
        return credentials.Certificate(settings.firebase_credentials_file)
    # Aquí entran las credenciales configuradas por gcloud / entorno GCP
    return credentials.ApplicationDefault()


cred = _get_firebase_credentials()
firebase_app = firebase_admin.initialize_app(cred, {
    "projectId": settings.firebase_project_id,
})
print("Firebase initialized with project ID:", settings.firebase_project_id)
print("Using Firebase credentials from:", firebase_app.credential.__class__.__name__)
print("Firebase app name:", firebase_app.name)
print("Firebase app options:", firebase_app.options)


def verify_firebase_token(id_token: str) -> dict:
    """
    Verifica un ID Token de Firebase y devuelve el payload decodificado.
    Lanza excepción si el token es inválido o está revocado.
    """
    decoded = firebase_auth.verify_id_token(
        id_token,
        app=firebase_app,
        check_revoked=True,
    )
    return decoded