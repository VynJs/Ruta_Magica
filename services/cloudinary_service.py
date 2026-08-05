import os
import uuid

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def subir_imagen(ruta_local: str, carpeta: str = "ruta_magica") -> dict:
    """
    Sube una imagen local a Cloudinary.

    Devuelve un diccionario: {"url": <secure_url>, "public_id": <public_id>}
    o lanza una excepción si algo falla (falta de credenciales, archivo
    inválido, sin conexión, etc.) — el llamador debe capturarla con try/except.
    """
    resultado = cloudinary.uploader.upload(
        ruta_local,
        folder=carpeta,
        public_id=str(uuid.uuid4()),
        overwrite=True,
    )
    return {
        "url": resultado.get("secure_url"),
        "public_id": resultado.get("public_id"),
    }


def eliminar_imagen(public_id: str) -> bool:
    """Elimina una imagen de Cloudinary por su public_id. True si se eliminó."""
    if not public_id:
        return False
    resultado = cloudinary.uploader.destroy(public_id)
    return resultado.get("result") == "ok"