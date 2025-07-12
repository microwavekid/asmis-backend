"""
Authentication API Router for ASMIS.

Provides endpoints for user authentication including login
and token refresh for the MVP.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from ..database.connection import get_db_session
from ..auth.auth_service import (
    login_user, 
    refresh_user_token,
    AuthenticationError,
    UserNotFoundError,
    InvalidCredentialsError,
    InactiveUserError,
    NoTenantAssociationError
)
from ..auth.jwt_service import TokenPair
from ..auth.models import AuthContext


# Create router
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


# Request/Response models
class LoginRequest(BaseModel):
    """Login request payload."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response with tokens and user info."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: dict  # Basic user info


class RefreshRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str


class RefreshResponse(BaseModel):
    """Token refresh response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes


class ErrorResponse(BaseModel):
    """Error response format."""
    detail: str
    error_code: Optional[str] = None


@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        403: {"model": ErrorResponse, "description": "Account inactive"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db_session)
) -> LoginResponse:
    """
    Authenticate user and return JWT tokens.
    
    This endpoint validates user credentials and returns both
    access and refresh tokens for authenticated sessions.
    
    For MVP, this is the only authentication endpoint needed
    since accounts are admin-provisioned.
    """
    try:
        # Authenticate and get tokens
        token_pair, auth_context = login_user(
            db=db,
            email=request.email,
            password=request.password
        )
        
        # Return tokens and basic user info
        return LoginResponse(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
            token_type=token_pair.token_type,
            expires_in=token_pair.expires_in,
            user={
                "id": auth_context.user_id,
                "email": auth_context.email,
                "tenant_id": auth_context.tenant_id,
                "role": auth_context.role
            }
        )
        
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    except InactiveUserError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support."
        )
    except NoTenantAssociationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no company association. Please contact support."
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        # Log the error in production
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )


@router.post(
    "/refresh",
    response_model=RefreshResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid refresh token"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db_session)
) -> RefreshResponse:
    """
    Generate new access token from refresh token.
    
    This endpoint allows clients to obtain a new access token
    when the current one expires, without requiring re-authentication.
    """
    try:
        # Generate new access token
        new_access_token = refresh_user_token(
            db=db,
            refresh_token=request.refresh_token
        )
        
        if not new_access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        return RefreshResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=1800  # 30 minutes
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (like 401 from token validation)
        raise
    except Exception as e:
        # Log the error in production for unexpected errors only
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )


# Optional: Health check endpoint for auth service
@router.get("/health")
async def auth_health():
    """Check if authentication service is running."""
    return {"status": "ok", "service": "authentication"}