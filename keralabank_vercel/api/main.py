from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import text
from xml.sax.saxutils import escape
from functools import lru_cache

# Import database and models
from database import SessionLocal, engine, Base
import models
import crud

SMA_CATEGORIES = ("sma0", "sma1", "sma2", "npa1", "npa2", "d1", "d2", "d3")

app = FastAPI(title="KeralaBank API")

# CORS configuration for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "KeralaBank API is running on Vercel"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "keralabank-api"}

# Authentication endpoint
@app.get("/login")
def login(emp_id: str, password: str, db: Session = Depends(get_db)):
    try:
        user = crud.authenticate_user(db, emp_id, password)
        if not user:
            return {"status": "error", "message": "Invalid credentials"}
        
        return {
            "status": "success",
            "user": {
                "emp_id": user.emp_id,
                "name": user.name,
                "designation": user.designation,
                "branch_code": user.branch_code,
                "phone": user.phone,
                "avatar": user.avatar
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# SMA Data endpoint
@app.get("/sma-data/{branch_code}")
def get_sma_data(branch_code: str, db: Session = Depends(get_db)):
    try:
        sma_data = crud.get_branch_sma_data(db, branch_code)
        if not sma_data:
            return {"error": "Branch data not found"}
        
        result = {}
        for category in SMA_CATEGORIES:
            result[category] = {
                "opening_number": getattr(sma_data, f"{category}_number", 0) or 0,
                "outstanding_amount": getattr(sma_data, f"{category}_outstanding", 0) or 0,
                "as_of_date": "2024-01-01",
                "number_collected": getattr(sma_data, f"{category}_number_collected", 0) or 0,
                "amount_collected": getattr(sma_data, f"{category}_amount_collected", 0) or 0,
                "number_previous": getattr(sma_data, f"{category}_number_previous", 0) or 0,
                "amount_previous": getattr(sma_data, f"{category}_amount_previous", 0) or 0,
                "numbertotal_collected": getattr(sma_data, f"{category}_numbertotal_collected", 0) or 0,
                "amounttotal_collected": getattr(sma_data, f"{category}_amounttotal_collected", 0) or 0,
                "number_balance": getattr(sma_data, f"{category}_number_balance", 0) or 0,
                "amount_balance": getattr(sma_data, f"{category}_amount_balance", 0) or 0,
            }
        
        return result
    except Exception as e:
        return {"error": str(e)}

# Collections endpoint
@app.get("/collections/{branch_code}/{category}")
def get_collections(branch_code: str, category: str, db: Session = Depends(get_db)):
    try:
        if category not in SMA_CATEGORIES:
            return {"error": "Invalid category"}
        
        sma_data = crud.get_branch_sma_data(db, branch_code)
        if not sma_data:
            return {"error": "Branch data not found"}
        
        return {
            "previous_day": {
                "number": getattr(sma_data, f"{category}_number_previous", 0) or 0,
                "amount": getattr(sma_data, f"{category}_amount_previous", 0) or 0
            },
            "today": {
                "number": getattr(sma_data, f"{category}_number_collected", 0) or 0,
                "amount": getattr(sma_data, f"{category}_amount_collected", 0) or 0
            },
            "total_month": {
                "number": getattr(sma_data, f"{category}_numbertotal_collected", 0) or 0,
                "amount": getattr(sma_data, f"{category}_amounttotal_collected", 0) or 0
            }
        }
    except Exception as e:
        return {"error": str(e)}

# Save collection endpoint
@app.post("/save-collection")
def save_collection(
    branch_code: str = Form(...),
    category: str = Form(...),
    number: int = Form(...),
    amount: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if category not in SMA_CATEGORIES:
            return {"error": "Invalid category"}
        
        crud.save_daily_collection(db, branch_code, category, number, amount)
        return {"status": "success", "message": "Collection saved"}
    except Exception as e:
        return {"error": str(e)}

# Messages endpoint
@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    try:
        messages = crud.get_all_messages(db)
        return messages
    except Exception as e:
        return {"error": str(e)}

# Send message endpoint
@app.post("/messages")
def send_message(emp_id: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    try:
        crud.create_message(db, emp_id, content)
        return {"status": "success", "message": "Message sent"}
    except Exception as e:
        return {"error": str(e)}

# Branches endpoint
@app.get("/branches")
def get_branches(db: Session = Depends(get_db)):
    try:
        branches = crud.get_all_branches(db)
        return branches
    except Exception as e:
        return {"error": str(e)}

# Staff endpoint
@app.get("/employees/{branch_id}")
def get_staff(branch_id: str, db: Session = Depends(get_db)):
    try:
        staff = crud.get_staff_by_branch(db, branch_id)
        return staff
    except Exception as e:
        return {"error": str(e)}

# Loan actions endpoints
@app.get("/loan-actions/{loan_number}")
def get_loan_actions(loan_number: str, db: Session = Depends(get_db)):
    try:
        loan = crud.get_loan_actions(db, loan_number)
        if not loan:
            return {"error": "Loan not found"}
        return loan
    except Exception as e:
        return {"error": str(e)}

@app.post("/loan-actions")
def create_loan_actions(
    loan_number: str = Form(...),
    action1: str = Form(...),
    action1_date: str = Form(...),
    action2: str = Form(...),
    action2_date: str = Form(...),
    action3: str = Form(...),
    action3_date: str = Form(...),
    action4: str = Form(...),
    action4_date: str = Form(...),
    action5: str = Form(...),
    action5_date: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        loan_data = {
            "loan_number": loan_number,
            "action1": action1,
            "action1_date": action1_date,
            "action2": action2,
            "action2_date": action2_date,
            "action3": action3,
            "action3_date": action3_date,
            "action4": action4,
            "action4_date": action4_date,
            "action5": action5,
            "action5_date": action5_date,
        }
        crud.create_loan_actions(db, loan_data)
        return {"status": "success", "message": "Loan actions created"}
    except Exception as e:
        return {"error": str(e)}

@app.put("/loan-actions/{loan_number}")
def update_loan_actions(
    loan_number: str,
    action1: str = Form(...),
    action1_date: str = Form(...),
    action2: str = Form(...),
    action2_date: str = Form(...),
    action3: str = Form(...),
    action3_date: str = Form(...),
    action4: str = Form(...),
    action4_date: str = Form(...),
    action5: str = Form(...),
    action5_date: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        loan_data = {
            "action1": action1,
            "action1_date": action1_date,
            "action2": action2,
            "action2_date": action2_date,
            "action3": action3,
            "action3_date": action3_date,
            "action4": action4,
            "action4_date": action4_date,
            "action5": action5,
            "action5_date": action5_date,
        }
        crud.update_loan_actions(db, loan_number, loan_data)
        return {"status": "success", "message": "Loan actions updated"}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/loan-actions/{loan_number}")
def delete_loan_actions(loan_number: str, db: Session = Depends(get_db)):
    try:
        crud.delete_loan_actions(db, loan_number)
        return {"status": "success", "message": "Loan actions deleted"}
    except Exception as e:
        return {"error": str(e)}

# Error reports endpoint
@app.get("/reports/{user_id}")
def get_user_reports(user_id: str, db: Session = Depends(get_db)):
    try:
        reports = crud.get_user_reports(db, user_id)
        return reports
    except Exception as e:
        return {"error": str(e)}

@app.get("/reports/all")
def get_all_reports(db: Session = Depends(get_db)):
    try:
        reports = crud.get_all_reports(db)
        return reports
    except Exception as e:
        return {"error": str(e)}

@app.post("/reports")
def create_report(
    emp_id: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        crud.create_error_report(db, emp_id, description)
        return {"status": "success", "message": "Report created"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/reports/{report_id}/resolve")
def resolve_report(
    report_id: int,
    ho_id: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        crud.resolve_report(db, report_id, ho_id)
        return {"status": "success", "message": "Report resolved"}
    except Exception as e:
        return {"error": str(e)}

# Document upload endpoint
@app.post("/upload-doc")
def upload_document(
    emp_id: str = Form(...),
    reason: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Save file to temporary directory
        os.makedirs("tmp", exist_ok=True)
        file_path = f"tmp/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create document record
        crud.create_document(db, emp_id, file.filename, file_path, reason)
        return {"status": "success", "message": "Document uploaded"}
    except Exception as e:
        return {"error": str(e)}

# Circulars endpoint
@app.get("/circulars")
def get_circulars(db: Session = Depends(get_db)):
    try:
        circulars = crud.get_all_circulars(db)
        return circulars
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload-circular")
def upload_circular(
    emp_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        os.makedirs("tmp", exist_ok=True)
        file_path = f"tmp/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        crud.create_circular(db, emp_id, file.filename, file_path)
        return {"status": "success", "message": "Circular uploaded"}
    except Exception as e:
        return {"error": str(e)}

# Consolidation links endpoint
@app.get("/consolidation-links")
def get_consolidation_links(db: Session = Depends(get_db)):
    try:
        links = crud.get_consolidation_links(db)
        return links
    except Exception as e:
        return {"error": str(e)}

@app.post("/consolidation-links")
def create_consolidation_link(
    emp_id: str = Form(...),
    heading: str = Form(...),
    link_url: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        crud.create_consolidation_link(db, emp_id, heading, link_url)
        return {"status": "success", "message": "Link created"}
    except Exception as e:
        return {"error": str(e)}

# Finacle help endpoint
@app.get("/finacle-help")
def get_finacle_help(db: Session = Depends(get_db)):
    try:
        help_entries = crud.get_finacle_help(db)
        return help_entries
    except Exception as e:
        return {"error": str(e)}

@app.post("/finacle-help")
def create_finacle_help(
    emp_id: str = Form(...),
    section_title: str = Form(...),
    menu_code: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        crud.create_finacle_help(db, emp_id, section_title, menu_code, description)
        return {"status": "success", "message": "Help entry created"}
    except Exception as e:
        return {"error": str(e)}

# Urgent messages endpoint
@app.get("/urgent")
def get_urgent_messages(db: Session = Depends(get_db)):
    try:
        urgent_messages = crud.get_urgent_messages(db)
        return urgent_messages
    except Exception as e:
        return {"error": str(e)}

@app.post("/urgent")
def create_urgent_message(
    emp_id: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        crud.create_urgent_message(db, emp_id, content)
        return {"status": "success", "message": "Urgent message created"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/urgent/seen")
def mark_urgent_as_seen(
    emp_id: str = Form(...),
    urgent_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        crud.mark_urgent_as_seen(db, emp_id, urgent_id)
        return {"status": "success", "message": "Urgent message marked as seen"}
    except Exception as e:
        return {"error": str(e)}

# Profile update endpoint
@app.post("/update-profile")
def update_profile(
    emp_id: str = Form(...),
    name: str = Form(...),
    designation: str = Form(...),
    phone: str = Form(...),
    branch_code: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        crud.update_employee_profile(db, emp_id, name, designation, phone, branch_code)
        return {"status": "success", "message": "Profile updated"}
    except Exception as e:
        return {"error": str(e)}

# Password update endpoint
@app.post("/update-password")
def update_password(
    emp_id: str = Form(...),
    new_pwd: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        crud.update_employee_password(db, emp_id, new_pwd)
        return {"status": "success", "message": "Password updated"}
    except Exception as e:
        return {"error": str(e)}

# Avatar upload endpoint
@app.post("/upload-avatar")
def upload_avatar(
    emp_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        os.makedirs("tmp", exist_ok=True)
        file_path = f"tmp/avatars/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        avatar_url = f"tmp/avatars/{file.filename}"
        crud.update_employee_avatar(db, emp_id, avatar_url)
        return {"status": "success", "avatar": avatar_url}
    except Exception as e:
        return {"error": str(e)}

# For Vercel serverless deployment
handler = app

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
