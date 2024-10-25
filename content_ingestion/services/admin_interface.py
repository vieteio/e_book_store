from fastapi import UploadFile
from models.ingestion_job import IngestionJob
from services.format_validator import FormatValidator
from services.metadata_processor import MetadataProcessor
from services.quality_assurance import QualityAssurance
from services.drm_service import DRMService
from services.content_distribution import ContentDistribution
from services.catalog_management import CatalogManagement
from services.notification_service import NotificationService
from services.analytics_service import AnalyticsService
import asyncio

class AdminInterface:
    def __init__(self):
        self.format_validator = FormatValidator()
        self.metadata_processor = MetadataProcessor()
        self.quality_assurance = QualityAssurance()
        self.drm_service = DRMService()
        self.content_distribution = ContentDistribution()
        self.catalog_management = CatalogManagement()
        self.notification_service = NotificationService()
        self.analytics_service = AnalyticsService()
        self.job_progress = {}

    def create_ingestion_job(self, metadata: dict) -> str:
        job = IngestionJob(**metadata)
        # TODO: Save job to database
        self.job_progress[job.id] = {"status": "created", "progress": 0}
        return job.id

    async def upload_manuscript(self, job_id: str, file: UploadFile) -> dict:
        self.job_progress[job_id] = {"status": "uploading", "progress": 10}
        # TODO: Implement file upload to S3
        file_path = f"s3://manuscripts/{job_id}/{file.filename}"
        
        # Start ingestion process
        await self.process_manuscript(job_id, file_path)
        return {"status": "success", "message": "Ingestion process started"}

    async def process_manuscript(self, job_id: str, file_path: str):
        try:
            self.job_progress[job_id] = {"status": "validating", "progress": 20}
            validation_result = self.format_validator.validate_format(file_path)
            if not validation_result['is_valid']:
                self.job_progress[job_id] = {"status": "failed", "progress": 0, "error": "Invalid file format"}
                return

            self.job_progress[job_id] = {"status": "converting", "progress": 30}
            converted_file = self.format_validator.convert_format(file_path)

            self.job_progress[job_id] = {"status": "extracting metadata", "progress": 40}
            metadata = self.metadata_processor.extract_metadata(converted_file)
            enriched_metadata = self.metadata_processor.enrich_metadata(metadata)
            self.metadata_processor.store_metadata(job_id, enriched_metadata)

            self.job_progress[job_id] = {"status": "quality assurance", "progress": 50}
            qa_results = self.quality_assurance.perform_qa_checks(converted_file)
            if not qa_results['passed']:
                self.job_progress[job_id] = {"status": "human QA required", "progress": 60}
                self.quality_assurance.route_to_human_qa(job_id)
                return

            self.job_progress[job_id] = {"status": "applying DRM", "progress": 70}
            protected_file = self.drm_service.apply_drm(converted_file)
            
            self.job_progress[job_id] = {"status": "distributing", "progress": 80}
            s3_status = self.content_distribution.upload_to_s3(protected_file)
            cdn_status = self.content_distribution.distribute_to_cdn(s3_status['s3_location'])
            
            self.job_progress[job_id] = {"status": "updating catalog", "progress": 90}
            self.catalog_management.update_catalog(job_id, enriched_metadata)
            preview_link = self.catalog_management.generate_preview_link(job_id)

            self.notification_service.notify_author(metadata['author_id'], "Your book has been successfully ingested!")
            self.notification_service.notify_internal_team("content_team", f"New book ingested: {metadata['title']}")

            self.analytics_service.update_ingestion_analytics(job_id, {
                "ingestion_time": "TODO: calculate time",
                "file_size": "TODO: get file size",
                "genre": metadata['genre']
            })

            self.job_progress[job_id] = {"status": "completed", "progress": 100, "preview_link": preview_link}
        except Exception as e:
            self.job_progress[job_id] = {"status": "failed", "progress": 0, "error": str(e)}

    def monitor_ingestion_progress(self, job_id: str) -> dict:
        return self.job_progress.get(job_id, {"status": "not found", "progress": 0})
