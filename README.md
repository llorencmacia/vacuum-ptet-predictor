# Ejector App

FastAPI-based ejector performance predictor.

## Run with Docker

```bash
git clone https://github.com/your-user/ejector-app.git
cd ejector-app
docker build -t ejector-app .
docker run -p 8000:8000 ejector-app
```

Then open:

http://localhost:8000

## Tech Stack
- FastAPI
- Uvicorn
- Matplotlib
- NumPy
- Dockerized deployment