from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
import datetime

class Branch(Base):
    __tablename__ = "branches"
    branch_id = Column(String, primary_key=True, index=True)
    branch_name = Column(String, nullable=False)
    employees = relationship("Employee", back_populates="branch")

class Employee(Base):
    __tablename__ = "employees"
    emp_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    branch_code = Column(String, ForeignKey("branches.branch_id"), nullable=False)
    phone = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    branch = relationship("Branch", back_populates="employees")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(String, ForeignKey("employees.emp_id"))
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Add this relationship to link to Employee details
    sender = relationship("Employee")

class Report(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, completed, cancelled
    resolved_by = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    timestamp = Column(DateTime)

class Document(Base):
    __tablename__ = "documents"
    doc_id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String, ForeignKey("employees.emp_id"))
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    reason = Column(String, nullable=True)   # <-- new field
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    employee = relationship("Employee")

class BranchSMAData(Base):
    __tablename__ = "branch_sma_data"
    branch_code = Column(String, ForeignKey("branches.branch_id"), primary_key=True)
    sma0_number = Column(Integer, default=0)
    sma0_outstanding = Column(Integer, default=0)
    sma1_number = Column(Integer, default=0)
    sma1_outstanding = Column(Integer, default=0)
    sma2_number = Column(Integer, default=0)
    sma2_outstanding = Column(Integer, default=0)
    npa1_number = Column(Integer, default=0)
    npa1_outstanding = Column(Integer, default=0)
    npa2_number = Column(Integer, default=0)
    npa2_outstanding = Column(Integer, default=0)
    d1_number = Column(Integer, default=0)
    d1_outstanding = Column(Integer, default=0)
    d2_number = Column(Integer, default=0)
    d2_outstanding = Column(Integer, default=0)
    d3_number = Column(Integer, default=0)
    d3_outstanding = Column(Integer, default=0)
    # Total collection fields for maintaining running totals
    sma0_total_collection = Column(Integer, default=0)
    sma1_total_collection = Column(Integer, default=0)
    sma2_total_collection = Column(Integer, default=0)
    npa1_total_collection = Column(Integer, default=0)
    npa2_total_collection = Column(Integer, default=0)
    d1_total_collection = Column(Integer, default=0)
    d2_total_collection = Column(Integer, default=0)
    d3_total_collection = Column(Integer, default=0)
    as_on_date = Column(DateTime, default=datetime.datetime.utcnow)
    sma0_number_collected = Column(Integer, default=0)
    sma0_amount_collected = Column(Integer, default=0)
    sma1_number_collected = Column(Integer, default=0)
    sma1_amount_collected = Column(Integer, default=0)
    sma2_number_collected = Column(Integer, default=0)
    sma2_amount_collected = Column(Integer, default=0)
    npa1_number_collected = Column(Integer, default=0)
    npa1_amount_collected = Column(Integer, default=0)
    npa2_number_collected = Column(Integer, default=0)
    npa2_amount_collected = Column(Integer, default=0)
    d1_number_collected = Column(Integer, default=0)
    d1_amount_collected = Column(Integer, default=0)
    d2_number_collected = Column(Integer, default=0)
    d2_amount_collected = Column(Integer, default=0)
    d3_number_collected = Column(Integer, default=0)
    d3_amount_collected = Column(Integer, default=0)
    sma0_numbertotal_collected = Column(Integer, default=0)
    sma0_amounttotal_collected = Column(Integer, default=0)
    sma1_numbertotal_collected = Column(Integer, default=0)
    sma1_amounttotal_collected = Column(Integer, default=0)
    sma2_numbertotal_collected = Column(Integer, default=0)
    sma2_amounttotal_collected = Column(Integer, default=0)
    npa1_numbertotal_collected = Column(Integer, default=0)
    npa1_amounttotal_collected = Column(Integer, default=0)
    npa2_numbertotal_collected = Column(Integer, default=0)
    npa2_amounttotal_collected = Column(Integer, default=0)
    d1_numbertotal_collected = Column(Integer, default=0)
    d1_amounttotal_collected = Column(Integer, default=0)
    d2_numbertotal_collected = Column(Integer, default=0)
    d2_amounttotal_collected = Column(Integer, default=0)
    d3_numbertotal_collected = Column(Integer, default=0)
    d3_amounttotal_collected = Column(Integer, default=0)
    sma0_number_previous = Column(Integer, default=0)
    sma0_amount_previous = Column(Integer, default=0)
    sma1_number_previous = Column(Integer, default=0)
    sma1_amount_previous = Column(Integer, default=0)
    sma2_number_previous = Column(Integer, default=0)
    sma2_amount_previous = Column(Integer, default=0)
    npa1_number_previous = Column(Integer, default=0)
    npa1_amount_previous = Column(Integer, default=0)
    npa2_number_previous = Column(Integer, default=0)
    npa2_amount_previous = Column(Integer, default=0)
    d1_number_previous = Column(Integer, default=0)
    d1_amount_previous = Column(Integer, default=0)
    d2_number_previous = Column(Integer, default=0)
    d2_amount_previous = Column(Integer, default=0)
    d3_number_previous = Column(Integer, default=0)
    d3_amount_previous = Column(Integer, default=0)
    sma0_number_balance = Column(Integer, default=0)
    sma0_amount_balance = Column(Integer, default=0)
    sma1_number_balance = Column(Integer, default=0)
    sma1_amount_balance = Column(Integer, default=0)
    sma2_number_balance = Column(Integer, default=0)
    sma2_amount_balance = Column(Integer, default=0)
    npa1_number_balance = Column(Integer, default=0)
    npa1_amount_balance = Column(Integer, default=0)
    npa2_number_balance = Column(Integer, default=0)
    npa2_amount_balance = Column(Integer, default=0)
    d1_number_balance = Column(Integer, default=0)
    d1_amount_balance = Column(Integer, default=0)
    d2_number_balance = Column(Integer, default=0)
    d2_amount_balance = Column(Integer, default=0)
    d3_number_balance = Column(Integer, default=0)
    d3_amount_balance = Column(Integer, default=0)
    sma0_last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    sma1_last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    sma2_last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    npa1_last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    npa2_last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    d1_last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    d2_last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    d3_last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class LoanAction(Base):
    __tablename__ = "loan_actions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_number = Column(String, nullable=False, index=True)
    action1 = Column(String, nullable=True)
    action1_date = Column(String, nullable=True)
    action2 = Column(String, nullable=True)
    action2_date = Column(String, nullable=True)
    action3 = Column(String, nullable=True)
    action3_date = Column(String, nullable=True)
    action4 = Column(String, nullable=True)
    action4_date = Column(String, nullable=True)
    action5 = Column(String, nullable=True)
    action5_date = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Circular(Base):
    __tablename__ = "circulars"
    doc_id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String, ForeignKey("employees.emp_id"))
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    employee = relationship("Employee")

class ConsolidationLink(Base):
    __tablename__ = "consolidation_links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String, ForeignKey("employees.emp_id"))
    heading = Column(String, nullable=False)
    link_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    employee = relationship("Employee")

class FinacleHelp(Base):
    __tablename__ = "finacle_help"
    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String, ForeignKey("employees.emp_id"))
    section_title = Column(String, nullable=False)
    menu_code = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    employee = relationship("Employee")

class UrgentMessage(Base):
    __tablename__ = "urgent_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String, ForeignKey("employees.emp_id"))
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    employee = relationship("Employee")

class UrgentSeen(Base):
    __tablename__ = "urgent_seen"
    id = Column(Integer, primary_key=True, autoincrement=True)
    urgent_id = Column(Integer, ForeignKey("urgent_messages.id"))
    emp_id = Column(String, ForeignKey("employees.emp_id"))
    seen_at = Column(DateTime, default=datetime.datetime.utcnow)
    employee = relationship("Employee")
