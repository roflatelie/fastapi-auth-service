from uuid import UUID

from src.adapters.repositories.aws_ses_repository import AWSSesRepository


class VerificationEmailUsecase:

    def __init__(self, aws_repository: AWSSesRepository):
        self.aws_repository = aws_repository

    async def send_verification_email(self, user_id: UUID, email: str) -> dict:
        link = f"http://localhost:8080/users/service/verify_email/{user_id}"
        email_data = await self.aws_repository.send_verification_email(link, email)
        return email_data
