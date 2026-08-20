from fastapi import APIRouter


router = APIRouter(
    tags=["Health"]
)


@router.get(
    "/health",
    summary="Health check"
)
def health_check():
    return {
        "status": "healthy",
        "message": "Research Management API is running"
    }