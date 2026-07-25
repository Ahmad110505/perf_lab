import os
import csv
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.reports.models import Report, ReportStatus, ReportFormat
from app.modules.reports.repository import report_repository
from app.modules.reports.schemas import ReportCreate
from app.modules.metrics.models import NormalizedMetric

STORAGE_DIR = os.path.join(os.getcwd(), "storage", "reports")

class ReportService:
    def create_report_request(self, db: Session, project_id: int, user_id: int, report_in: ReportCreate) -> Report:
        report_data = {
            "project_id": project_id,
            "created_by_user_id": user_id,
            "name": report_in.name,
            "format": report_in.format,
            "period_start": report_in.period_start,
            "period_end": report_in.period_end,
            "status": ReportStatus.PENDING,
        }
        report = report_repository.create(db, obj_in=report_data)
        
        self.generate_report_file(db, report_id=report.id)
        
        return report

    def generate_report_file(self, db: Session, report_id: int) -> Report:
        report = report_repository.get(db, id=report_id)
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Report {report_id} not found")

        os.makedirs(STORAGE_DIR, exist_ok=True)
        filename = f"report_proj_{report.project_id}_{report.id}.csv"
        file_path = os.path.join(STORAGE_DIR, filename)

        try:
            query = db.query(NormalizedMetric).filter(NormalizedMetric.project_id == report.project_id)
            if report.period_start:
                query = query.filter(NormalizedMetric.metric_date >= report.period_start)
            if report.period_end:
                query = query.filter(NormalizedMetric.metric_date <= report.period_end)

            metrics = query.all()

            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Metric Date", "Metric Type", "Value", "Source Provider"])
                for m in metrics:
                    writer.writerow([
                        m.metric_date.isoformat() if m.metric_date else "",
                        m.metric_type,
                        m.value,
                        m.source_provider
                    ])

            report.file_path = file_path
            report.status = ReportStatus.COMPLETED
            db.commit()
            db.refresh(report)

        except Exception as e:
            db.rollback()
            report = report_repository.get(db, id=report_id)
            if report:
                report.status = ReportStatus.FAILED
                db.commit()
            raise e

        return report

report_service = ReportService()
