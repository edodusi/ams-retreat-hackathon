# Documentation Index

Welcome to the Storyblok Voice Assistant documentation! This guide will help you navigate all available documentation resources.

## 📚 Quick Links

### Getting Started
- **[Setup Guide](SETUP.md)** - Installation, configuration, and first-time setup
- **[Project README](../README.md)** - Project overview and quick start

### Reference Documentation
- **[API Documentation](API.md)** - Complete API reference with examples
- **[Features Guide](FEATURES.md)** - Detailed feature documentation and usage
- **[cURL Tests](CURL_TESTS.md)** - Backend testing with cURL commands

### Specifications
- **[Technical Specs](../SPECS.md)** - Architecture and technical specifications
- **[Development Guidelines](../GUIDELINES.md)** - Guidelines for development
- **[OpenAPI Spec](openapi.yaml)** - OpenAPI 3.0 specification

---

## 📖 Documentation Overview

### [Setup Guide](SETUP.md)
Complete installation and configuration instructions including:
- Prerequisites and requirements
- Python environment setup
- Dependency installation
- Environment configuration
- Running the application
- Troubleshooting common issues
- Browser requirements

**Start here if:** You're setting up the project for the first time.

---

### [API Documentation](API.md)
Comprehensive API reference covering:
- All endpoints with request/response schemas
- Error handling and status codes
- Integration examples (JavaScript, Python, cURL)
- Configuration options
- Performance considerations
- Security notes

**Use this when:** You need to integrate with or understand the backend API.

---

### [Features Guide](FEATURES.md)
Detailed documentation of all features:
- Voice input/output capabilities
- Natural language conversation
- Content search functionality
- Story preview cards
- Chat interface design
- Keyboard navigation
- Accessibility features
- Technical implementation details

**Use this when:** You want to understand what the system can do and how to use it.

---

### [cURL Testing Guide](CURL_TESTS.md)
Practical testing examples:
- Health check tests
- Conversation endpoint tests
- Multi-turn conversation examples
- Debug endpoint tests
- Error testing scenarios
- Performance testing commands
- Batch testing scripts

**Use this when:** You need to test backend functionality without the UI.

---

### [Technical Specifications](../SPECS.md)
Project architecture and specifications:
- System architecture diagram
- Technology stack details
- API integration examples
- Conversation flow patterns
- Accessibility requirements (WCAG 2.1 AA)
- Development phases
- Demo script

**Use this when:** You need to understand the technical architecture and design decisions.

---

### [Development Guidelines](../GUIDELINES.md)
Best practices for development:
- Documentation standards
- Testing requirements
- API documentation updates
- Communication guidelines
- Workflow summary

**Use this when:** Contributing to or extending the project.

---

### [OpenAPI Specification](openapi.yaml)
Machine-readable API specification:
- OpenAPI 3.0 format
- All endpoints and schemas
- Request/response examples
- Can be imported into tools like Postman

**Use this when:** You need to generate API clients or import into API tools.

---

## 🚀 Quick Navigation by Task

### I want to...

#### Set up the project for the first time
1. Read [Setup Guide](SETUP.md)
2. Follow installation steps
3. Test with [cURL Tests](CURL_TESTS.md)

#### Understand how to use the application
1. Read [Features Guide](FEATURES.md)
2. Review conversation examples in [API Documentation](API.md)
3. Try the live application

#### Integrate with the API
1. Read [API Documentation](API.md)
2. Review integration examples
3. Test with [cURL Tests](CURL_TESTS.md)
4. Import [OpenAPI Spec](openapi.yaml) into your tools

#### Test the backend
1. Start with [cURL Tests](CURL_TESTS.md)
2. Use debug endpoints (see [API Documentation](API.md))
3. Check [Setup Guide](SETUP.md) for troubleshooting

#### Understand the architecture
1. Read [Technical Specifications](../SPECS.md)
2. Review system diagrams
3. Check technology stack details

#### Contribute to the project
1. Read [Development Guidelines](../GUIDELINES.md)
2. Review [Technical Specifications](../SPECS.md)
3. Follow testing practices in guidelines

---

## 📝 Documentation Format

All documentation follows these conventions:

### Markdown Standards
- Headers use `#` syntax
- Code blocks use triple backticks with language identifiers
- Links are relative within the project
- Tables for structured data
- Lists for sequential or grouped items

### Code Examples
- Shell commands use `bash` syntax
- API examples include full requests and responses
- Language-specific examples labeled (JavaScript, Python, cURL)
- Expected outputs shown after commands

### Accessibility
- Clear, concise language
- Descriptive headings and subheadings
- Table of contents for long documents
- Examples illustrate concepts
- Links clearly indicate destination

---

## 🔄 Keeping Documentation Updated

When making changes to the project:

1. **Backend API changes** → Update:
   - [API Documentation](API.md)
   - [OpenAPI Spec](openapi.yaml)
   - [cURL Tests](CURL_TESTS.md) if applicable

2. **New features** → Update:
   - [Features Guide](FEATURES.md)
   - [Project README](../README.md)
   - [API Documentation](API.md) if API changes

3. **Configuration changes** → Update:
   - [Setup Guide](SETUP.md)
   - [Project README](../README.md)

4. **Architecture changes** → Update:
   - [Technical Specifications](../SPECS.md)
   - [Project README](../README.md)

---

## 🆘 Getting Help

### Documentation Issues
If you find errors or gaps in documentation:
1. Check if information exists in another doc
2. Refer to inline code comments
3. Review example code in the project
4. Check commit history for context

### Technical Issues
1. Check [Setup Guide](SETUP.md) troubleshooting section
2. Review error messages carefully
3. Test with [cURL Tests](CURL_TESTS.md)
4. Enable DEBUG mode for verbose logging

### Feature Questions
1. Check [Features Guide](FEATURES.md)
2. Review [Technical Specifications](../SPECS.md)
3. Try the interactive API docs at `/docs`

---

## 📦 Additional Resources

### Interactive Documentation
When the server is running:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### External Resources
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Storyblok Strata Docs](https://www.storyblok.com/docs/strata)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Alpine.js Documentation](https://alpinejs.dev/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

## 📊 Documentation Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| Setup Guide | ✅ Complete | Oct 30, 2025 |
| API Documentation | ✅ Complete | Oct 30, 2025 |
| Features Guide | ✅ Complete | Oct 30, 2025 |
| cURL Tests | ✅ Complete | Oct 30, 2025 |
| Technical Specs | ✅ Complete | Oct 30, 2025 |
| OpenAPI Spec | ✅ Complete | Oct 30, 2025 |
| Development Guidelines | ✅ Complete | Oct 30, 2025 |

---

**Project Version:** 1.0.0  
**Documentation Version:** 1.0.0  
**Last Updated:** October 30, 2025

---

*For questions or improvements, refer to the [Development Guidelines](../GUIDELINES.md).*