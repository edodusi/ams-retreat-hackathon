#!/bin/bash

# Test script for analytical and conversational features
# Tests: content type filtering, analysis/count queries, conversational flow

BASE_URL="http://localhost:8000"
API_URL="${BASE_URL}/api/conversation"

echo "=========================================="
echo "Testing Analytical & Conversational Features"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test counter
TEST_NUM=0

# Function to run a test
run_test() {
    TEST_NUM=$((TEST_NUM + 1))
    local test_name=$1
    local message=$2
    local history=$3
    
    echo -e "${BLUE}Test ${TEST_NUM}: ${test_name}${NC}"
    echo -e "${YELLOW}Message: ${message}${NC}"
    
    if [ -z "$history" ]; then
        PAYLOAD="{\"message\": \"${message}\", \"conversation_history\": []}"
    else
        PAYLOAD="{\"message\": \"${message}\", \"conversation_history\": ${history}}"
    fi
    
    echo "Request:"
    echo "$PAYLOAD" | jq '.' 2>/dev/null || echo "$PAYLOAD"
    echo ""
    
    RESPONSE=$(curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD")
    
    echo -e "${GREEN}Response:${NC}"
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
    
    # Extract key fields
    ACTION=$(echo "$RESPONSE" | jq -r '.action // "none"')
    MESSAGE=$(echo "$RESPONSE" | jq -r '.message // "none"')
    RESULT_COUNT=$(echo "$RESPONSE" | jq -r '.results.stories | length // 0')
    ANALYSIS_COUNT=$(echo "$RESPONSE" | jq -r '.analysis.count // "N/A"')
    
    echo ""
    echo -e "${GREEN}Summary:${NC}"
    echo "  Action: $ACTION"
    echo "  Result Count: $RESULT_COUNT"
    echo "  Analysis Count: $ANALYSIS_COUNT"
    echo ""
    echo "=========================================="
    echo ""
    
    # Wait a bit between tests
    sleep 1
}

# Test 1: Analytical query (count)
echo -e "${YELLOW}=== Scenario 1: Analytical Queries ===${NC}"
echo ""

run_test "Count articles about Drupal" \
    "how many articles mention drupal?"

run_test "Check existence of blog posts" \
    "do we have any blog posts about React?"

run_test "Count with specific content type" \
    "how many pages mention AI?"

echo ""
echo -e "${YELLOW}=== Scenario 2: Content Type Filtering ===${NC}"
echo ""

run_test "Search for articles only" \
    "find 5 articles about marketing"

run_test "Search for blog posts only" \
    "show me blog posts about technology"

run_test "Search for pages" \
    "find pages about our company"

echo ""
echo -e "${YELLOW}=== Scenario 3: Clarification Requests ===${NC}"
echo ""

run_test "Ambiguous content type" \
    "find stories about marketing"

run_test "Generic search without type" \
    "show me content about javascript"

echo ""
echo -e "${YELLOW}=== Scenario 4: Conversational Flow (Analyze → List) ===${NC}"
echo ""

# First, analyze
echo -e "${BLUE}Step 1: Analyze${NC}"
ANALYZE_RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d '{"message": "how many articles mention GraphQL?", "conversation_history": []}')

echo "$ANALYZE_RESPONSE" | jq '.'

ANALYZE_MESSAGE=$(echo "$ANALYZE_RESPONSE" | jq -r '.message')
ANALYZE_ACTION=$(echo "$ANALYZE_RESPONSE" | jq -r '.action')
ANALYZE_COUNT=$(echo "$ANALYZE_RESPONSE" | jq -r '.analysis.count // 0')

echo ""
echo "Step 1 Summary:"
echo "  Action: $ANALYZE_ACTION"
echo "  Count: $ANALYZE_COUNT"
echo "  Message: $ANALYZE_MESSAGE"
echo ""

# Build conversation history for next request
HISTORY="[{\"role\": \"user\", \"content\": \"how many articles mention GraphQL?\"}, {\"role\": \"assistant\", \"content\": \"${ANALYZE_MESSAGE}\"}]"

# Then, list
echo -e "${BLUE}Step 2: List analyzed results${NC}"
sleep 1

LIST_RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"yes please show them\", \"conversation_history\": ${HISTORY}}")

echo "$LIST_RESPONSE" | jq '.'

LIST_ACTION=$(echo "$LIST_RESPONSE" | jq -r '.action')
LIST_COUNT=$(echo "$LIST_RESPONSE" | jq -r '.results.stories | length // 0')

echo ""
echo "Step 2 Summary:"
echo "  Action: $LIST_ACTION"
echo "  Stories Returned: $LIST_COUNT"
echo ""
echo "=========================================="
echo ""

echo ""
echo -e "${YELLOW}=== Scenario 5: Search with Refinement ===${NC}"
echo ""

# First, search
echo -e "${BLUE}Step 1: Initial search${NC}"
SEARCH_RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d '{"message": "find 10 articles about web development", "conversation_history": []}')

echo "$SEARCH_RESPONSE" | jq '.'

SEARCH_COUNT=$(echo "$SEARCH_RESPONSE" | jq -r '.results.stories | length // 0')
echo "Initial search returned: $SEARCH_COUNT stories"
echo ""

# Build history
SEARCH_MSG=$(echo "$SEARCH_RESPONSE" | jq -r '.message')
HISTORY2="[{\"role\": \"user\", \"content\": \"find 10 articles about web development\"}, {\"role\": \"assistant\", \"content\": \"${SEARCH_MSG}\"}]"

# Then, refine
echo -e "${BLUE}Step 2: Refine results${NC}"
sleep 1

REFINE_RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"from these, show me only the ones about React\", \"conversation_history\": ${HISTORY2}}")

echo "$REFINE_RESPONSE" | jq '.'

REFINE_COUNT=$(echo "$REFINE_RESPONSE" | jq -r '.results.stories | length // 0')
echo "Refined search returned: $REFINE_COUNT stories"
echo ""
echo "=========================================="
echo ""

echo ""
echo -e "${GREEN}=== All Tests Complete ===${NC}"
echo ""
echo "Summary:"
echo "  Total tests run: ${TEST_NUM}"
echo ""
echo "Key Features Tested:"
echo "  ✓ Analytical queries (count)"
echo "  ✓ Content type filtering"
echo "  ✓ Clarification requests"
echo "  ✓ Conversational flow (analyze → list)"
echo "  ✓ Search refinement"
echo ""
echo "Check the responses above to verify correct behavior."
echo ""