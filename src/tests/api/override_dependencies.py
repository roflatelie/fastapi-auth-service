from src.core.exceptions import RequestProcessingException


async def override_send_email_dependency_success(link: str, email: str) -> None:
    pass


async def override_send_email_dependency_exception(link: str, email: str) -> None:
    raise RequestProcessingException
