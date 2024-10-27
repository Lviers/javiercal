from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def calculator_form(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def calculate(request: Request):
    form_data = await request.form()
    num1 = float(form_data.get("num1"))
    num2 = float(form_data.get("num2"))
    operator = form_data.get("operator")

    try:
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise HTTPException(status_code=400, detail="Cannot divide by zero")
            result = num1 / num2
        else:
            raise HTTPException(status_code=400, detail="Invalid operator")
    except HTTPException as e:
        return templates.TemplateResponse("main.html", {"request": request, "error": e.detail})

    return templates.TemplateResponse("main.html", {"request": request, "result": result})

