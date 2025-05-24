from repositories.apartment_repository import ApartmentRepository
from models.user import User
from fastapi import HTTPException

async def require_owner_or_admin(
    apartment_id: str,
    current_user: User,
    apartment_repository: ApartmentRepository,
):
    if current_user.admin:
        return  # доступ разрешён

    apartment = await apartment_repository.get_by_id(apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")

    if apartment.ownerId != current_user.userId:
        raise HTTPException(status_code=403, detail="Not authorized to access this apartment")