# Sistema DIRENS - Teacher Management System

## Overview

This is a desktop application for managing teachers in the DIRENS (Diretoria de Ensino da Aeronáutica) educational system. Built with Python and Tkinter, it provides a comprehensive interface for managing teacher data across multiple Brazilian Air Force educational institutions. The system handles teacher registration, data validation, backup management, statistics generation, and export capabilities with a focus on Brazilian Air Force educational requirements.

## User Preferences

Preferred communication style: Simple, everyday language.

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