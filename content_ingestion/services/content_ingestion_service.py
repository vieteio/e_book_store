import httpx
from .format_validator import validate_format, convert_format

async def ingest_content(job_id: str, file: bytes):
    # Validate format
    validation_result = await validate_format(file)
    if not validation_result['is_valid']:
        await flag_manual_review(job_id, f"Invalid format: {validation_result['error']}")
        return

    # Convert format
    conversion_result = await convert_format(file)
    if not conversion_result['success']:
        await flag_manual_review(job_id, f"Conversion failed: {conversion_result['error']}")
        return

    # Continue with the rest of the ingestion process...

async def flag_manual_review(job_id: str, issue: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://format-validator-service/flag-for-manual-review",
            json={"job_id": job_id, "issue": issue}
        )
        response.raise_for_status()
