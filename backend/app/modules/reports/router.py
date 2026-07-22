import os
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.reports.schemas import ReportCreate, ReportResponse, ReportListResponse
from app.modules.reports.services import report_service
from app.modules.reports.repository import report_repository

router = APIRouter(prefix="/projects", tags=["reports"])

@router.post("/{project_id}/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    project_id: int,
    report_in: ReportCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Generate a new report for a project."""
    return report_service.create_report_request(db, project_id=project_id, user_id=current_user_id, report_in=report_in)

@router.get("/{project_id}/reports", response_model=ReportListResponse)
def list_reports(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """List all reports generated for a project."""
    reports, total = report_repository.get_by_project_id(db, project_id=project_id, skip=skip, limit=limit)
    return {"items": reports, "total": total}

@router.get("/{project_id}/reports/{report_id}/download")
def download_report(
    project_id: int,
    report_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Download the generated report CSV file."""
    report = report_repository.get(db, id=report_id)
    if not report or report.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found for this project")

    if not report.file_path or not os.path.exists(report.file_path):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Report file is missing or not yet generated")

    return FileResponse(
        path=report.file_path,
        media_type="text/csv",
        filename=os.path.basename(report.file_path)
    )
