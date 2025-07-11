# ⚽ QUCOON Football Academy Career Assistant

A comprehensive AI-powered career guidance system for aspiring football players and coaches, built with Streamlit and Google's Gemini AI.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The QUCOON Football Academy Career Assistant is an intelligent chatbot system designed to help football enthusiasts navigate their career paths. Whether you're an aspiring player or coach, this system provides personalized guidance, recruitment evaluation, and mentorship support.

## ✨ Features

### For Players
- **Player Recruitment System**: Comprehensive evaluation process for aspiring players
- **Eligibility Assessment**: Automated screening based on age, experience, and skill level
- **Career Mentorship**: Personalized guidance for existing academy players
- **Application Processing**: Streamlined application workflow with validation

### For Coaches
- **Coach Recruitment**: Specialized evaluation for coaching positions
- **Certification Validation**: Verification of coaching credentials and experience
- **Career Development**: Mentorship for existing coaching staff
- **Professional Assessment**: Comprehensive evaluation of coaching background

### General Features
- **AI-Powered Conversations**: Natural language processing using Google Gemini AI
- **Multi-Modal Support**: Handles both new applicants and existing members
- **Real-time Validation**: Instant feedback on application data
- **Secure Data Handling**: Professional data management and storage
- **Interactive Interface**: User-friendly Streamlit web application

## 🛠 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Google Gemini AI API key


### User Flow

1. **Initial Welcome**: Users identify as "existing" members with IDs or "new" applicants
2. **Existing Users**: Login with talent ID (P001, C001, etc.) for personalized mentorship
3. **New Applicants**: Choose between Player or Coach development paths
4. **Evaluation Process**: Complete comprehensive assessment forms
5. **Results**: Receive eligibility determination and next steps

### Player Application Process

Players must provide:
- Personal information (name, age, position)
- Experience details (years played, current level)
- Physical attributes (height, weight, pace, dominant foot)
- Achievements and video highlights
- Availability for relocation

### Coach Application Process

Coaches must provide:
- Personal information (name, age, experience)
- Certifications and qualifications
- Coaching specialty and previous roles
- Professional references
- Availability dates

## 📁 File Structure

```
qucoon-football-academy/
├── appp.py                 # Main Streamlit application
├── config.py               # Configuration and API keys
├── requirements.txt        # Python dependencies
├── mylogoo.png            # Academy logo
├── utils.py               # Utility functions
├── data_manager.py        # Database operations
├── gemini_service.py      # Google Gemini AI integration
├── player_agent.py        # Player recruitment logic
├── coach_agent.py         # Coach recruitment logic
└── README.md              # This file
```

### Core Components

- **appp.py**: Main application orchestrating the entire user experience
- **player_agent.py**: Handles player recruitment and evaluation
- **coach_agent.py**: Manages coach recruitment and assessment
- **gemini_service.py**: Integrates with Google Gemini AI for conversational responses
- **data_manager.py**: Manages user data and academy database
- **utils.py**: Common utility functions for validation and error handling


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
