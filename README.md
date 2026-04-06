# TradeWiseAI

AI-Powered Tariff Intelligence and Trade Optimization System

Overview
TradeWise AI is a backend-driven tariff intelligence engine designed to process international trade data and enable structured tariff analysis at the HS6 level.
The system transforms raw tariff datasets into a normalized master tariff matrix and integrates an AI-based HS code classification layer for product description mapping.
The objective is to provide a scalable foundation for intelligent trade decision-making and automated tariff comparison.

Problem Statement
Importers and analysts face several challenges:
Complex HS classification systems
Fragmented tariff datasets across countries
Manual tariff lookup processes
Inefficient multi-country comparison

TradeWise AI addresses these issues through automated preprocessing, structured datasets, and AI-driven classification.

System Architecture
1. Data Processing Pipeline
Raw tariff data extraction from WITS
HS8 to HS6 normalization
Country-specific tariff cleaning
Master tariff matrix construction
Structured CSV generation for backend use

2. AI Classification Layer
NLP-based product description encoding
Embedding-based semantic similarity matching
HS6 prediction from natural language input

4. Tariff Lookup Engine
Efficient tariff retrieval using structured datasets
Multi-country comparison at HS6 level
Backend-ready integration via API

Project Structure
makethon/
│
├── backend2/
│   ├── main.py
│   ├── hs_classifier.py
│   ├── hs_routes.py
│   ├── tariff_loader.py
│
├── data/
│   ├── processed/
│   ├── raw/  (ignored)
│
├── dataset/
│   ├── build_tariff_matrix.py
│   ├── preprocess_tariffs.py
│   ├── final_clean_master.py
│   ├── sanity_check.py
│
├── .gitignore
└── README.md

Countries Covered

MFN tariff data processed at HS6 level for:
India – China
India – Japan
India – Republic of Korea
India – UAE
India – Vietnam

Technology Stack
Python
FastAPI
Pandas
Sentence Transformers (HuggingFace)
Uvicorn

CSV-based structured datasets

Key Features:
HS6 code classification from product descriptions
Master tariff matrix generation
Clean multi-country tariff comparison
Structured backend-ready data architecture
=======
# TradeWiseAI
>>>>>>> 191a11fb59924c4d0a380867a28e6c841ca87214
