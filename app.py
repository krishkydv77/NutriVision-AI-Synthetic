from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles ### for static folder(html,css,js)
from fastapi.templating import Jinja2Templates ### for rendring html output from fastapi 
from routes.predict import router as predict_router

app = FastAPI(title="NutriVision - AI Nutrition Analyzer", version="1.0.0")

# Mount Static Files & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include Prediction Router
app.include_router(predict_router)

@app.get("/")
async def render_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    uvicorn.run("app:app", host="0.0.0.0", port=8000) 