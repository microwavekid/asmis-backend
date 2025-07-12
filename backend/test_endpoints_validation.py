#!/usr/bin/env python3
"""
Endpoint Validation Test - Checks that our new endpoints are properly configured
without requiring a running server.
"""

import sys
sys.path.insert(0, '.')

from app.main import app
from app.routers.deals import router as deals_router
import json


def test_endpoint_registration():
    """Test that our new endpoints are registered in the router."""
    print("🔍 Checking Deal Router Endpoints...\n")
    
    endpoints = []
    for route in deals_router.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            for method in route.methods:
                endpoints.append({
                    'method': method,
                    'path': route.path,
                    'name': route.name if hasattr(route, 'name') else 'unknown'
                })
    
    # Check for our new endpoints
    required_endpoints = [
        ('PUT', '/api/v1/deals/{deal_id}', 'update_deal'),
        ('DELETE', '/api/v1/deals/{deal_id}', 'delete_deal')
    ]
    
    print("📋 Registered Endpoints:")
    print("-" * 60)
    for ep in endpoints:
        print(f"{ep['method']:8} {ep['path']:40} {ep['name']}")
    
    print("\n✅ Checking Required Endpoints:")
    print("-" * 60)
    
    all_found = True
    for method, path, name in required_endpoints:
        found = any(
            ep['method'] == method and ep['path'] == path and ep['name'] == name 
            for ep in endpoints
        )
        status = "✅" if found else "❌"
        print(f"{status} {method:8} {path:40} {name}")
        if not found:
            all_found = False
    
    return all_found


def test_endpoint_details():
    """Test endpoint configurations."""
    print("\n\n📝 Endpoint Configuration Details:\n")
    
    # Find our specific endpoints
    for route in deals_router.routes:
        if hasattr(route, 'name') and route.name in ['update_deal', 'delete_deal']:
            print(f"🔧 Endpoint: {route.name}")
            print(f"   Path: {route.path}")
            print(f"   Methods: {list(route.methods) if hasattr(route, 'methods') else 'N/A'}")
            
            # Check response model
            if hasattr(route, 'response_model'):
                print(f"   Response Model: {route.response_model}")
            
            # Check dependencies
            if hasattr(route, 'dependencies'):
                print(f"   Dependencies: {len(route.dependencies) if route.dependencies else 0}")
            
            # Check status code for DELETE
            if route.name == 'delete_deal' and hasattr(route, 'status_code'):
                print(f"   Status Code: {route.status_code}")
            
            print()


def test_schema_validation():
    """Test that required schemas exist."""
    print("\n📊 Schema Validation:\n")
    
    try:
        from app.schemas.deals import DealUpdate, DealResponse
        print("✅ DealUpdate schema imported successfully")
        print("✅ DealResponse schema imported successfully")
        
        # Check DealUpdate fields
        print("\n📋 DealUpdate Schema Fields:")
        for field_name, field_info in DealUpdate.model_fields.items():
            required = field_info.is_required()
            print(f"   - {field_name}: {'required' if required else 'optional'}")
        
    except ImportError as e:
        print(f"❌ Schema import failed: {e}")


def test_auth_integration():
    """Test authentication dependency configuration."""
    print("\n\n🔐 Authentication Integration:\n")
    
    from app.routers.router_config import get_auth_dependency, get_auth_mode
    
    auth_mode = get_auth_mode()
    print(f"Current Auth Mode: {auth_mode}")
    
    auth_dep = get_auth_dependency()
    print(f"Auth Dependency Function: {auth_dep.__name__}")
    print(f"Auth Dependency Module: {auth_dep.__module__}")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("🧪 Deal Management API - Endpoint Validation")
    print("=" * 60)
    
    # Test 1: Endpoint Registration
    endpoints_ok = test_endpoint_registration()
    
    # Test 2: Endpoint Details
    test_endpoint_details()
    
    # Test 3: Schema Validation
    test_schema_validation()
    
    # Test 4: Auth Integration
    test_auth_integration()
    
    print("\n" + "=" * 60)
    if endpoints_ok:
        print("✅ All required endpoints are properly registered!")
    else:
        print("❌ Some endpoints are missing!")
    print("=" * 60)


if __name__ == "__main__":
    main()