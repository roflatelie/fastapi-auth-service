from abc import ABC, abstractmethod


class AWSRepository(ABC):

    @abstractmethod
    async def send_verification_email(self, link: str, email: str):
        pass

    @abstractmethod
    async def send_reset_password_email(self, link: str, email: str):
        pass
