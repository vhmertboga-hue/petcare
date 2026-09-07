import os
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.file import File

try:
    import boto3
except Exception:
    boto3 = None


async def save_file_for_animal(db: AsyncSession, owner_id: int, animal_id: int, filename: str, content: bytes, mimetype: Optional[str] = None) -> File:
    s3_bucket = os.getenv("S3_BUCKET")
    s3_key = None
    url = None

    if boto3 and s3_bucket:
        s3 = boto3.client("s3")
        import uuid

        s3_key = f"health_docs/{uuid.uuid4().hex}/{filename}"
        try:
            s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=content, ContentType=mimetype or "application/octet-stream")
            url = f"https://{s3_bucket}.s3.amazonaws.com/{s3_key}"
        except Exception:
            s3_key = None
            url = None

    f = File(owner_id=owner_id, animal_id=animal_id, filename=filename, file_data=content if not s3_key else None, s3_key=s3_key, url=url, mimetype=mimetype)
    db.add(f)
    await db.flush()
    await db.commit()
    await db.refresh(f)
    return f
