# Vacuum Ejector App for calculating the Predicted Total Evacuation Time (PTET)

FastAPI-based ejector performance predictor.

## Run with Docker

```bash
git clone https://github.com/llorencmacia/vacuum-ptet-predictor.git
cd vacuum-ptet-predictor
docker build -t vacuum-ptet-predictor .
docker run -p 8000:8000 vacuum-ptet-predictor
```

Then open:

http://localhost:8000

## Tech Stack
- FastAPI
- Uvicorn
- PlotPy
- NumPy
- Dockerized deployment
