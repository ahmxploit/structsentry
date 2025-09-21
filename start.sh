#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --port 8002 &
PYTHONPATH=$(pwd) streamlit run ui/dashboard.py --server.port 8502 --server.headless true