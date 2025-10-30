#!/usr/bin/env python3
"""Test script to verify context-aware refinement fix"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Testing Context-Aware Refinement Fix")
print("=" * 60)

# Test 1: Initial search
print("\n📤 Request 1: Initial search")
request1 = {
    "message": "find the articles that mention the drupal migration",
    "conversation_history": []
}

try:
    response1 = requests.post(
        f"{BASE_URL}/api/conversation",
        json=request1,
        timeout=30
    )
    
    if response1.status_code == 200:
        data1 = response1.json()
        story_count = len(data1.get("results", {}).get("stories", [])) if data1.get("results") else 0
        print(f"✅ Response 1: {story_count} stories returned")
        print(f"   Message: {data1.get('message', '')[:80]}...")
        
        if story_count > 0:
            print(f"   First story: {data1['results']['stories'][0]['name']}")
    else:
        print(f"❌ Request 1 failed: {response1.status_code}")
        print(response1.text)
        exit(1)

except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend. Is it running?")
    print("   Start with: python -m uvicorn backend.main:app --reload")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test 2: Refinement query
print("\n📤 Request 2: Refinement query")
request2 = {
    "message": "of those, get 2 articles that mention the CLI",
    "conversation_history": [
        {"role": "user", "content": "find the articles that mention the drupal migration"},
        {"role": "assistant", "content": data1.get('message', '')}
    ]
}

try:
    response2 = requests.post(
        f"{BASE_URL}/api/conversation",
        json=request2,
        timeout=30
    )
    
    if response2.status_code == 200:
        data2 = response2.json()
        story_count2 = len(data2.get("results", {}).get("stories", [])) if data2.get("results") else 0
        message2 = data2.get('message', '')
        
        print(f"✅ Response 2: {story_count2} stories returned")
        print(f"   Message: {message2[:80]}...")
        
        # Check if refinement worked
        if "don't have access to previous results" in message2:
            print("\n❌ REFINEMENT FAILED - Session context not found!")
            print("   The fix didn't work. Session key not matching.")
        elif story_count2 > 0 and story_count2 <= story_count:
            print(f"\n✅ REFINEMENT SUCCESSFUL!")
            print(f"   Filtered from {story_count} to {story_count2} stories")
            for i, story in enumerate(data2['results']['stories'][:2], 1):
                print(f"   {i}. {story['name']}")
        elif story_count2 == 0:
            print("\n⚠️  No stories matched the filter criteria (0 results)")
            print("   This is OK if 'CLI' doesn't appear in any stories")
        else:
            print(f"\n⚠️  Unexpected result count: {story_count2}")
    else:
        print(f"❌ Request 2 failed: {response2.status_code}")
        print(response2.text)
        exit(1)

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)

