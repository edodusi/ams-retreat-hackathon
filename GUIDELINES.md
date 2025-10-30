# AI Coding Agent Guidelines

This document provides guidelines for AI coding agents working on this project.

## Documentation

- After implementing each new feature, provide proper documentation in markdown format
- Documentation files should be placed in the `/docs` folder
- Include:
  - Feature overview
  - Usage examples
  - Configuration options (if applicable)
  - Any dependencies or prerequisites

## Testing

### Minimal Unit Testing
- Provide minimal unit tests for fundamental features
- Focus on core functionality and critical paths
- Tests should be clear and maintainable

### Feature Verification
- **Backend features**: Test using `curl` commands after implementation
  - Include example `curl` commands in the feature documentation
  - Verify all HTTP methods (GET, POST, PUT, DELETE, etc.)
  - Test both success and error cases
- **Frontend features**: Quick unit tests are sufficient
  - Focus on component behavior and user interactions
  - No need for extensive integration tests unless specifically requested

## API Documentation

### OpenAPI Specifications
- Create OpenAPI specs for all new backend endpoints
- Place specs in the appropriate location (e.g., `/docs/api` or `/openapi`)
- **Important**: Update OpenAPI specs every time endpoints are modified
  - This includes changes to:
    - Request/response schemas
    - Query parameters
    - Path parameters
    - Headers
    - Status codes

## Communication

### No Unnecessary Summaries
- Do not provide lengthy summaries after completing a feature
- Keep responses focused and concise
- Only provide information that is actionable or necessary

### Ask When Unclear
- If requirements are ambiguous or unclear, **STOP and ask the developer**
- Do not make assumptions about:
  - Implementation details not specified
  - Technology choices when multiple options exist
  - Business logic or requirements
- It's better to clarify upfront than to implement incorrectly

## Workflow Summary

1. Implement the feature
2. Write minimal unit tests for core functionality
3. Test the feature:
   - Backend: Use `curl` commands
   - Frontend: Run unit tests
4. Create/update OpenAPI specs (backend only)
5. Document the feature in `/docs`
6. Move to the next task (no need to summarize)

---

*These guidelines help maintain consistency and quality while optimizing the development workflow.*