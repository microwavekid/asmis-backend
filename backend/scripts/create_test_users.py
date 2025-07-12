#!/usr/bin/env python3
"""
Create test users for ASMIS MVP.

This script creates admin-provisioned user accounts for testing
the JWT authentication system.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from app.database.config import get_database_settings
from app.database.models import User, Tenant, TenantUser
from app.auth.auth_service import create_user
from app.auth.password_service import generate_temp_password


def create_test_data():
    """Create test tenants and users for MVP testing."""
    
    # Get database URL from settings
    settings = get_database_settings()
    
    # Create database engine and session
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Create test tenants if they don't exist
        test_tenants = [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Acme Corp",
                "slug": "acme-corp",
                "is_active": True
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "name": "Beta Industries", 
                "slug": "beta-industries",
                "is_active": True
            }
        ]
        
        for tenant_data in test_tenants:
            existing_tenant = db.query(Tenant).filter(
                Tenant.id == tenant_data["id"]
            ).first()
            
            if not existing_tenant:
                tenant = Tenant(**tenant_data)
                db.add(tenant)
                print(f"✅ Created tenant: {tenant_data['name']}")
            else:
                print(f"ℹ️  Tenant already exists: {tenant_data['name']}")
        
        db.commit()
        
        # Create test users
        test_users = [
            {
                "email": "alice@acme.com",
                "username": "alice",
                "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
                "role": "admin",
                "name": "Alice Admin"
            },
            {
                "email": "bob@acme.com",
                "username": "bob",
                "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
                "role": "member",
                "name": "Bob Member"
            },
            {
                "email": "david@beta.com",
                "username": "david",
                "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
                "role": "owner",
                "name": "David Owner"
            }
        ]
        
        print("\n📝 Creating test users...\n")
        
        for user_data in test_users:
            # Check if user already exists
            existing_user = db.query(User).filter(
                User.email == user_data["email"]
            ).first()
            
            if existing_user:
                print(f"ℹ️  User already exists: {user_data['email']}")
                continue
            
            # Generate temporary password
            temp_password = generate_temp_password()
            
            # Create user
            try:
                user = create_user(
                    db=db,
                    email=user_data["email"],
                    username=user_data["username"],
                    password=temp_password,
                    tenant_id=user_data["tenant_id"],
                    role=user_data["role"]
                )
                
                print(f"✅ Created user: {user_data['email']}")
                print(f"   Username: {user_data['username']}")
                print(f"   Password: {temp_password}")
                print(f"   Role: {user_data['role']}")
                print(f"   Tenant: {user_data['tenant_id'][:8]}...")
                print()
                
            except Exception as e:
                print(f"❌ Failed to create user {user_data['email']}: {str(e)}")
        
        print("\n🎯 Test data creation complete!")
        print("\n⚠️  IMPORTANT: Save these passwords securely and share with test users.")
        print("Users should be prompted to change passwords on first login in production.")
        
    except Exception as e:
        print(f"❌ Error creating test data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 ASMIS Test User Creation Script")
    print("=" * 40)
    
    # Check if JWT auth is configured
    use_jwt = os.getenv("USE_JWT_AUTH", "false").lower() == "true"
    
    if not use_jwt:
        print("\n⚠️  WARNING: JWT authentication is not enabled.")
        print("Set USE_JWT_AUTH=true to use real authentication.")
        response = input("\nContinue anyway? (y/n): ")
        
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    
    create_test_data()