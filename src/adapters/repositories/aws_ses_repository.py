import boto3
from src.core import settings as creds
from src.core.exceptions import RequestProcessingException
from src.decorators.make_async_decorator import make_async
from src.ports.repositories.aws_repository import AWSRepository


class AWSSesRepository(AWSRepository):
    def __init__(self, actual_credentials: dict):
        self.ses = boto3.client("ses", **actual_credentials)

    @make_async
    def _base_send_email(self, message: str, subject: str, email: str) -> dict:
        try:
            response = self.ses.send_email(
                Source=creds.source_email,
                Destination={
                    "ToAddresses": (email,),
                },
                Message={
                    "Body": {
                        "Text": {
                            "Data": message,
                        }
                    },
                    "Subject": {
                        "Data": subject,
                    },
                },
            )
            return response
        except self.ses.exceptions.BotoCoreError:
            raise RequestProcessingException

    async def send_verification_email(self, link: str, email: str):
        message = f"You need to verify your email. Click link to verify it {link}"
        subject = "Email confirmation"
        await self._base_send_email(message=message, subject=subject, email=email)

    async def send_reset_password_email(self, link: str, email: str):
        message = f"Follow this link to reset your password. {link}"
        subject = "Resetting password"
        await self._base_send_email(message=message, subject=subject, email=email)
