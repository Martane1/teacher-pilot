# Sistema DIRENS - Teacher Management System

## Overview

This is a desktop application for managing teachers in the DIRENS (Diretoria de Ensino da Aeronáutica) educational system. Built with Python and Tkinter, it provides a comprehensive interface for managing teacher data across multiple Brazilian Air Force educational institutions. The system handles teacher registration, data validation, backup management, statistics generation, and export capabilities with a focus on Brazilian Air Force educational requirements.

## Recent Changes

**August 15, 2025**
- Simplified teacher registration form by removing unnecessary academic fields:
  - Removed "Graduação" (Graduation) field
  - Removed "Instituição da Graduação" (Graduation Institution) field  
  - Removed "Curso Pós-graduação" (Post-graduation Course) field
  - Removed "Instituição Pós" (Post-graduation Institution) field
- Added comprehensive accent support for Portuguese characters:
  - Added accent buttons (´, ^, ~, ç) to both name field and search field
  - Support for á, é, í, ó, ú, â, ê, ô, ã, õ, ç characters
- Updated validation system to accommodate simplified form structure
- Improved form layout and window sizing for better usability
- **Added DIRENS to login options**: DIRENS now appears as a school option in login screen
- **Created Schools Overview feature**:
  - Added "Todas as Escolas" button in toolbar and menu
  - New dedicated window showing all DIRENS schools with details
  - Displays school information, codes, addresses, and contact details
  - Export functionality for schools list
- **Simplified discipline registration form**:
  - Reduced to only 3 fields: Código, Nome da Disciplina, Requisito Específico
  - Larger text area for "Requisito Específico" field with scrollbar
  - Updated form validation for new simplified structure

## User Preferences

Preferred communication style: Simple, everyday language.
Accent Input: User requires ability to input Portuguese accent characters (á, é, í, ó, ú, â, ê, ô, ã, õ, ç) in name fields and search functionality using button-based accent system.

## System Architecture

### Core Architecture Pattern
The application follows a modular MVC-style architecture with clear separation of concerns:

- **Main Application (`main.py`)**: Entry point and system initialization
- **Core Logic (`core/`)**: Business logic and data processing
- **Interface Layer (`interface/`)**: Tkinter-based GUI components
- **Data Layer (`dados/`)**: Data persistence and management
- **Resources (`recursos/`)**: Configuration, constants, and utilities

### GUI Framework
**Tkinter Desktop Application**: Uses Python's built-in Tkinter library for cross-platform desktop GUI with modal windows and form-based interfaces. This choice provides simplicity and eliminates external GUI dependencies.

### Data Storage Strategy
**JSON File-based Storage**: All data is persisted in JSON files with file locking for concurrent access safety. This approach was chosen for:
- Zero database server dependencies
- Human-readable data format
- Easy backup and portability
- Simple deployment

### Authentication System
**File-based User Management**: User credentials are stored in encrypted JSON files with SHA-256 password hashing. Default admin accounts are automatically created for each school.

### Validation Layer
**Centralized Validation**: The `ValidatorManager` class handles all data validation including:
- Brazilian SIAPE (7-digit teacher ID) validation
- CPF (Brazilian tax ID) validation with checksum verification
- Date format validation
- Required field validation

### Export and Reporting
**Multi-format Export**: Supports both CSV and PDF export formats using:
- `csv` module for spreadsheet exports
- `reportlab` for PDF generation with tables and formatting

### Backup Management
**Automated Backup System**: Configurable backup schedules with:
- ZIP compression for storage efficiency
- Configurable retention policies
- Manual and automatic backup triggers

### History Tracking
**Audit Trail System**: Complete change history tracking with:
- Before/after value comparisons
- User attribution for all changes
- Timestamped modification logs

### Error Handling and Logging
**Comprehensive Logging**: Multi-level logging system with:
- File-based daily logs
- Console output for development
- Module-specific error tracking

## External Dependencies

### Core Python Libraries
- **tkinter**: GUI framework (built-in)
- **json**: Data serialization (built-in)
- **hashlib**: Password encryption (built-in)
- **datetime**: Date/time handling (built-in)
- **logging**: System logging (built-in)
- **threading**: Concurrent operations (built-in)

### Third-party Packages
- **filelock**: File locking for concurrent access safety
- **reportlab**: PDF generation and document formatting
- **matplotlib**: Statistical charts and graphs generation

### File System Dependencies
- **Local JSON files**: Primary data storage
- **Directory structure**: Organized data, logs, backups, and exports folders
- **Configuration files**: JSON-based system configuration

### Integration Points
- **Brazilian Educational System**: SIAPE teacher identification integration
- **Air Force Educational Network**: Multi-institution teacher management across AFA, CBNB, CIAAR, CTRB, ECE, EEAR, EPCAR, EAOAR, ECEMAR, and UNIFA
- **Government Standards**: CPF validation and Brazilian date formats