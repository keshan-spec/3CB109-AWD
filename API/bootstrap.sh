#!/bin/sh
export FLASK_ENV=development
export DATABASE_URL=postgresql://postgres:postgres@localhost/api_db
export JWT_SECRET_KEY=hhgaghhgsdhdhdd
python ./src/run.py