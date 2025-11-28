#!/usr/bin/env python3
"""
Test script for Prompt Management API.

This script demonstrates how to use the prompt management API endpoints.
Make sure the FastAPI server is running before executing this script.

Usage:
    python scripts/test_prompt_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(response, action):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{action}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
    else:
        print("Response: No content")
    print(f"{'='*60}\n")


def test_create_prompt():
    """Test creating a new prompt."""
    url = f"{BASE_URL}/prompts"
    data = {
        "name": "test_prompt_1",
        "content": "This is a test prompt for demonstration purposes."
    }
    response = requests.post(url, json=data)
    print_response(response, "CREATE PROMPT")
    return response


def test_get_all_prompts():
    """Test getting all prompts."""
    url = f"{BASE_URL}/prompts"
    response = requests.get(url)
    print_response(response, "GET ALL PROMPTS")
    return response


def test_get_all_prompts_filtered():
    """Test getting all prompts with filters."""
    url = f"{BASE_URL}/prompts?app_name=Video_Risk_Assessment&region=us-central1"
    response = requests.get(url)
    print_response(response, "GET ALL PROMPTS (FILTERED)")
    return response


def test_get_prompt_by_id(prompt_id):
    """Test getting a specific prompt by ID."""
    url = f"{BASE_URL}/prompts/{prompt_id}"
    response = requests.get(url)
    print_response(response, f"GET PROMPT BY ID ({prompt_id})")
    return response


def test_update_prompt(prompt_id):
    """Test updating a prompt."""
    url = f"{BASE_URL}/prompts/{prompt_id}"
    data = {
        "content": "This is the UPDATED content for the test prompt."
    }
    response = requests.put(url, json=data)
    print_response(response, f"UPDATE PROMPT ({prompt_id})")
    return response


def test_delete_prompt(prompt_id):
    """Test deleting a prompt."""
    url = f"{BASE_URL}/prompts/{prompt_id}"
    response = requests.delete(url)
    print_response(response, f"DELETE PROMPT ({prompt_id})")
    return response


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("PROMPT MANAGEMENT API TEST SUITE")
    print("="*60)
    
    # Test 1: Create a new prompt
    print("\n1. Creating a new prompt...")
    create_response = test_create_prompt()
    
    if create_response.status_code == 201:
        prompt_id = create_response.json()["id"]
        print(f"✅ Prompt created successfully with ID: {prompt_id}")
        
        # Test 2: Get all prompts
        print("\n2. Getting all prompts...")
        test_get_all_prompts()
        
        # Test 3: Get all prompts with filters
        print("\n3. Getting all prompts with filters...")
        test_get_all_prompts_filtered()
        
        # Test 4: Get prompt by ID
        print(f"\n4. Getting prompt by ID ({prompt_id})...")
        test_get_prompt_by_id(prompt_id)
        
        # Test 5: Update prompt
        print(f"\n5. Updating prompt ({prompt_id})...")
        update_response = test_update_prompt(prompt_id)
        if update_response.status_code == 200:
            print(f"✅ Prompt updated successfully. New version: {update_response.json()['version']}")
        
        # Test 6: Get updated prompt
        print(f"\n6. Verifying the update...")
        test_get_prompt_by_id(prompt_id)
        
        # Test 7: Delete prompt
        print(f"\n7. Deleting prompt ({prompt_id})...")
        delete_response = test_delete_prompt(prompt_id)
        if delete_response.status_code == 204:
            print(f"✅ Prompt deleted successfully")
        
        # Test 8: Verify deletion
        print(f"\n8. Verifying deletion...")
        verify_response = test_get_prompt_by_id(prompt_id)
        if verify_response.status_code == 404:
            print(f"✅ Confirmed: Prompt no longer exists")
        
    else:
        print(f"❌ Failed to create prompt. Status code: {create_response.status_code}")
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the FastAPI server is running on http://localhost:8000")
        print("\nTo start the server, run:")
        print("    uvicorn main:rest_api_app --reload")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
