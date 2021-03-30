from typing import List, Optional

from fastapi import APIRouter, Depends

from ..sec import FastAPISecurity, User

__all__ = ("make_router",)


def make_router(
    security: FastAPISecurity,
    *,
    user_details_url: str,
    user_details_tags: Optional[List[str]] = None,
) -> APIRouter:
    router = APIRouter()

    @router.get(
        user_details_url,
        # TODO: Uncomment these two lines once
        #       https://github.com/tiangolo/fastapi/pull/2841 has been merged
        #       and released.
        # response_model=User,
        # response_model_exclude={"auth": {"access_token"}},
        summary="Get user details",
        tags=user_details_tags or ["User"],
    )
    async def user_details(user: User = Depends(security.user_with_info)):
        return user.without_access_token()

    return router
