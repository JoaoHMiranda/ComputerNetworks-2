#!/bin/bash
python3 backend/app.py &
sleep 2
streamlit run frontend/streamlit_app.py --server.address=0.0.0.0 --server.port=8501