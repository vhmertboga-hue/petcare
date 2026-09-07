import os
from typing import Optional
import uuid

from backend.app.models.file import File


def _s3_client():
    import boto3

    endpoint = os.getenv("AWS_S3_ENDPOINT")
    return boto3.client(
        "s3",
        endpoint_url=endpoint if endpoint else None,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


async def upload_file_to_s3(db, upload_file, owner_id: Optional[int] = None):
    client = _s3_client()
    bucket = os.getenv("S3_BUCKET", "petcare")
    key = f"uploads/{uuid.uuid4()}-{upload_file.filename}"
    client.put_object(Bucket=bucket, Key=key, Body=await upload_file.read())
    url = f"{os.getenv('S3_PUBLIC_URL','')}/{key}"
    f = File(owner_id=owner_id, filename=upload_file.filename, s3_key=key, url=url, mimetype=upload_file.content_type)
    db.add(f)
    await db.flush()
    await db.commit()
    await db.refresh(f)
    return f


async def upload_file_to_db(db, upload_file, owner_id: Optional[int] = None):
    content = await upload_file.read()
    f = File(owner_id=owner_id, filename=upload_file.filename, content=content, mimetype=upload_file.content_type)
    db.add(f)
    await db.flush()
    await db.commit()
    await db.refresh(f)
    return f


async def store_upload(db, upload_file, owner_id: Optional[int] = None):
    if os.getenv("AWS_S3_ENDPOINT"):
        return await upload_file_to_s3(db, upload_file, owner_id)
    return await upload_file_to_db(db, upload_file, owner_id)
