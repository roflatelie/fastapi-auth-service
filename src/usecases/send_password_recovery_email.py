from src.adapters.repositories.aws_ses_repository import AWSSesRepository


class ResetPasswordEmailUsecase:

    def __init__(self, aws_repository: AWSSesRepository):
        self.aws_repository = aws_repository

    async def send_password_reset_email(self, user_id: str, email: str) -> dict:
        link = f"http://localhost:8080/users/service/reset_password/{user_id}"
        email_data = await self.aws_repository.send_reset_password_email(link, email)
        return email_data
