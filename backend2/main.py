from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.hs_routes import router as hs_router


app = FastAPI(
    title="TradeWise AI",
    description="AI-powered HS code classification and trade route optimization",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hs_router)

@app.get("/")
def root():
    return {"message": "TradeWise AI backend is running 🚀"}