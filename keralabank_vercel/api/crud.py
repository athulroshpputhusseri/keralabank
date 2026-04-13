from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
import json
import models
from models import Report

# ------------------- AUTH -------------------
def authenticate_user(db: Session, emp_id: str, password: str):
    """Verifies employee credentials."""
    return db.query(models.Employee).filter(
        models.Employee.emp_id == emp_id,
        models.Employee.password == password
    ).first()

# 
def get_all_branches(db: Session):
    return db.query(models.Branch).all()

#  EMPLOYEES -------------------
def get_employee_by_branch(db: Session, branch_code: str):
    """Retrieves all employees for a specific branch."""
    return db.query(models.Employee).filter(models.Employee.branch_code == branch_code).all()

def get_staff_by_branch(db: Session, branch_id: str):
    """Retrieves staff for a specific branch."""
    return db.query(models.Employee).filter(models.Employee.branch_code == branch_id).all()

# ------------------- MESSAGES -------------------
def create_message(db: Session, emp_id: str, content: str):
    """Creates a new message with current UTC timestamp."""
    msg = models.Message(
        sender_id=emp_id,
        content=content,
        timestamp = datetime.now(timezone.utc)
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session):
    """Retrieves all messages with sender details joined."""
    # We join Message -> Employee -> Branch to get all info in one go
    return db.query(models.Message).options(
        joinedload(models.Message.sender).joinedload(models.Employee.branch)
    ).order_by(models.Message.timestamp.asc()).all()

def get_all_messages(db: Session):
    """Retrieves all messages with sender details joined."""
    messages = get_messages(db)
    return [
        {
            "id": msg.id,
            "sender_id": msg.sender_id,
            "sender_name": msg.sender.name if msg.sender else "Unknown",
            "sender_branch": msg.sender.branch.branch_name if msg.sender and msg.sender.branch else "Unknown",
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
        }
        for msg in messages
    ]

def get_recent_messages(db: Session):
    """Retrieves messages with joined Employee and Branch data."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=12)
    return db.query(models.Message).options(
        joinedload(models.Message.sender).joinedload(models.Employee.branch)
    ).filter(models.Message.timestamp >= cutoff).all()

# ------------------- REPORTS -------------------
def create_report(db: Session, emp_id: str, description: str):
    report = Report(emp_id=emp_id, description=description, timestamp=datetime.now(timezone.utc))
    db.add(report)
    try:
        db.commit()
        db.refresh(report)
        return report
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create report: constraint violation.")

def create_error_report(db: Session, emp_id: str, description: str):
    """Creates an error report."""
    return create_report(db, emp_id, description)

def get_reports(db: Session, emp_id: str):
    """Retrieves all reports for a specific employee."""
    return db.query(models.Report).filter(models.Report.emp_id == emp_id).order_by(models.Report.timestamp.desc()).all()

def get_user_reports(db: Session, user_id: str):
    """Retrieves all reports for a specific user."""
    return get_reports(db, user_id)

def get_all_reports(db: Session):
    """Retrieves all reports submitted by all employees."""
    return db.query(models.Report).order_by(models.Report.timestamp.desc()).all()

def resolve_report(db: Session, report_id: int, ho_id: str):
    report = db.query(models.Report).filter(models.Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = "completed"
    report.resolved_by = ho_id
    report.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(report)
    return report

def cancel_report(db: Session, report_id: int, emp_id: str):
    report = db.query(models.Report).filter(
        models.Report.report_id == report_id,
        models.Report.emp_id == emp_id,
        models.Report.status == "pending"
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found or cannot be cancelled")
    report.status = "cancelled"
    db.commit()
    db.refresh(report)
    return report

# ------------------- SMA DATA -------------------
def get_branch_sma_data(db: Session, branch_code: str):
    """Retrieves SMA data for a specific branch."""
    return db.query(models.BranchSMAData).filter(models.BranchSMAData.branch_code == branch_code).first()

def save_daily_collection(db: Session, branch_code: str, category: str, collection_number: int, collection_amount: int):
    """Saves daily collection data for a specific category."""
    row = get_branch_sma_data(db, branch_code)
    if not row:
        raise HTTPException(status_code=404, detail="Branch SMA data not found")

    today = datetime.now(timezone.utc).date()
    opening_number = getattr(row, f"{category}_number", 0) or 0
    opening_amount = getattr(row, f"{category}_outstanding", 0) or 0
    current_number = getattr(row, f"{category}_number_collected", 0) or 0
    current_amount = getattr(row, f"{category}_amount_collected", 0) or 0
    total_number = getattr(row, f"{category}_numbertotal_collected", 0) or 0
    total_amount = getattr(row, f"{category}_amounttotal_collected", 0) or 0
    last_updated = getattr(row, f"{category}_last_updated", None)
    last_updated_date = last_updated.date() if last_updated else None

    # Check if we're on a new day
    if last_updated_date and last_updated_date < today:
        # Move yesterday's data to previous_day fields
        setattr(row, f"{category}_number_previous", current_number)
        setattr(row, f"{category}_amount_previous", current_amount)
        # Reset today's data for new day
        total_number = collection_number
        total_amount = collection_amount
    elif last_updated_date == today:
        # Same day, update totals
        total_number += collection_number - current_number
        total_amount += collection_amount - current_amount
    else:
        # First time entering data for this category
        total_number = collection_number
        total_amount = collection_amount

    setattr(row, f"{category}_number_collected", collection_number)
    setattr(row, f"{category}_amount_collected", collection_amount)
    setattr(row, f"{category}_numbertotal_collected", total_number)
    setattr(row, f"{category}_amounttotal_collected", total_amount)
    setattr(row, f"{category}_number_balance", opening_number - total_number)
    setattr(row, f"{category}_amount_balance", opening_amount - total_amount)
    setattr(row, f"{category}_last_updated", datetime.now(timezone.utc))
    db.commit()
    db.refresh(row)
    return row

# ------------------- LOAN ACTIONS -------------------
def get_loan_actions(db: Session, loan_number: str):
    """Retrieves loan actions for a specific loan number."""
    return db.query(models.LoanAction).filter(models.LoanAction.loan_number == loan_number).first()

def create_loan_actions(db: Session, loan_data: dict):
    """Creates new loan actions."""
    loan = models.LoanAction(
        loan_number=loan_data["loan_number"],
        action1=loan_data.get("action1"),
        action1_date=loan_data.get("action1_date"),
        action2=loan_data.get("action2"),
        action2_date=loan_data.get("action2_date"),
        action3=loan_data.get("action3"),
        action3_date=loan_data.get("action3_date"),
        action4=loan_data.get("action4"),
        action4_date=loan_data.get("action4_date"),
        action5=loan_data.get("action5"),
        action5_date=loan_data.get("action5_date")
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def update_loan_actions(db: Session, loan_number: str, loan_data: dict):
    """Updates existing loan actions."""
    loan = db.query(models.LoanAction).filter(models.LoanAction.loan_number == loan_number).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    loan.action1 = loan_data.get("action1", loan.action1)
    loan.action1_date = loan_data.get("action1_date", loan.action1_date)
    loan.action2 = loan_data.get("action2", loan.action2)
    loan.action2_date = loan_data.get("action2_date", loan.action2)
    loan.action3 = loan_data.get("action3", loan.action3)
    loan.action3_date = loan_data.get("action3_date", loan.action3)
    loan.action4 = loan_data.get("action4", loan.action4)
    loan.action4_date = loan_data.get("action4_date", loan.action4)
    loan.action5 = loan_data.get("action5", loan.action5)
    loan.action5_date = loan_data.get("action5_date", loan.action5)
    loan.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(loan)
    return loan

def delete_loan_actions(db: Session, loan_number: str):
    """Deletes loan actions."""
    loan = db.query(models.LoanAction).filter(models.LoanAction.loan_number == loan_number).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    db.delete(loan)
    db.commit()
    return loan

# ------------------- DOCUMENTS -------------------
def create_document(db: Session, emp_id: str, filename: str, filepath: str, reason: str):
    """Creates a document record."""
    doc = models.Document(
        emp_id=emp_id,
        filename=filename,
        filepath=filepath,
        reason=reason
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

# ------------------- CIRCULARS -------------------
def get_all_circulars(db: Session):
    """Retrieves all circulars."""
    return db.query(models.Circular).order_by(models.Circular.uploaded_at.desc()).all()

def create_circular(db: Session, emp_id: str, filename: str, filepath: str):
    """Creates a circular record."""
    circular = models.Circular(
        emp_id=emp_id,
        filename=filename,
        filepath=filepath
    )
    db.add(circular)
    db.commit()
    db.refresh(circular)
    return circular

# ------------------- CONSOLIDATION LINKS -------------------
def get_consolidation_links(db: Session):
    """Retrieves all consolidation links."""
    return db.query(models.ConsolidationLink).order_by(models.ConsolidationLink.created_at.desc()).all()

def create_consolidation_link(db: Session, emp_id: str, heading: str, link_url: str):
    """Creates a consolidation link."""
    link = models.ConsolidationLink(
        emp_id=emp_id,
        heading=heading,
        link_url=link_url
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

# ------------------- FINACLE HELP -------------------
def get_finacle_help(db: Session):
    """Retrieves all finacle help entries."""
    return db.query(models.FinacleHelp).order_by(models.FinacleHelp.created_at.desc()).all()

def create_finacle_help(db: Session, emp_id: str, section_title: str, menu_code: str, description: str):
    """Creates a finacle help entry."""
    help_entry = models.FinacleHelp(
        emp_id=emp_id,
        section_title=section_title,
        menu_code=menu_code,
        description=description
    )
    db.add(help_entry)
    db.commit()
    db.refresh(help_entry)
    return help_entry

# ------------------- URGENT MESSAGES -------------------
def get_urgent_messages(db: Session):
    """Retrieves all urgent messages."""
    return db.query(models.UrgentMessage).order_by(models.UrgentMessage.created_at.desc()).all()

def create_urgent_message(db: Session, emp_id: str, content: str):
    """Creates an urgent message."""
    urgent = models.UrgentMessage(
        emp_id=emp_id,
        content=content
    )
    db.add(urgent)
    db.commit()
    db.refresh(urgent)
    return urgent

def mark_urgent_as_seen(db: Session, emp_id: str, urgent_id: int):
    """Marks an urgent message as seen by an employee."""
    seen = models.UrgentSeen(
        urgent_id=urgent_id,
        emp_id=emp_id
    )
    db.add(seen)
    db.commit()
    db.refresh(seen)
    return seen

# ------------------- PROFILE MANAGEMENT -------------------
def update_employee_profile(db: Session, emp_id: str, name: str, designation: str, phone: str, branch_code: str):
    """Updates employee profile."""
    employee = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.name = name
    employee.designation = designation
    employee.phone = phone
    employee.branch_code = branch_code
    
    db.commit()
    db.refresh(employee)
    return employee

def update_employee_password(db: Session, emp_id: str, new_password: str):
    """Updates employee password."""
    employee = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.password = new_password
    
    db.commit()
    db.refresh(employee)
    return employee

def update_employee_avatar(db: Session, emp_id: str, avatar_url: str):
    """Updates employee avatar."""
    employee = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.avatar = avatar_url
    
    db.commit()
    db.refresh(employee)
    return employee
