from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router


app = FastAPI(title="Curso API - Segurança")
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)


# TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzI4OTQ2Njk5LCJpYXQiOjE3MjgzNDE4OTksInN1YiI6IjEifQ.6WbN-dCV0N07xcfchKAYX1E_advdqwGozyew1l14D8g
# TYPE: BEARER
