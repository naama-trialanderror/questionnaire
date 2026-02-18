#!/bin/bash
cd "$(dirname "$0")"
open "http://localhost:8501" &
streamlit run app.py
