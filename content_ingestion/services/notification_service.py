import boto3
import slack
import requests
from botocore.exceptions import ClientError
from typing import Optional
from enum import Enum

class NotificationPlatform(Enum):
    SLACK = "slack"
    TEAMS = "teams"
    BOTH = "both"

class NotificationService:
    def __init__(self, platform: NotificationPlatform = NotificationPlatform.SLACK):
        self.ses_client = boto3.client('ses', region_name='us-east-1')
        self.platform = platform
        
        # Initialize Slack client if needed
        if platform in [NotificationPlatform.SLACK, NotificationPlatform.BOTH]:
            self.slack_client = slack.WebClient(token="YOUR_SLACK_BOT_TOKEN")
        
        # Initialize Teams webhook URL if needed
        if platform in [NotificationPlatform.TEAMS, NotificationPlatform.BOTH]:
            self.teams_webhook_url = "YOUR_TEAMS_WEBHOOK_URL"

    def notify_author(self, author_id, message):
        # Implementation for notifying the author
        pass

    def notify_internal_team(self, team_id, message):
        # Implementation for notifying internal teams
        pass

    def _send_slack_notification(self, subject: str, body: str) -> Optional[str]:
        """Send notification to Slack"""
        try:
            self.slack_client.chat_postMessage(
                channel="#content-ingestion",
                text=f"<!here> {subject}\n\n{body}"
            )
            return None
        except Exception as e:
            return f"Slack notification failed: {str(e)}"

    def _send_teams_notification(self, subject: str, body: str) -> Optional[str]:
        """Send notification to Microsoft Teams"""
        try:
            teams_message = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": "0076D7",
                "summary": subject,
                "sections": [{
                    "activityTitle": subject,
                    "activitySubtitle": "Manual Review Required",
                    "text": body
                }]
            }
            
            response = requests.post(
                self.teams_webhook_url,
                json=teams_message
            )
            response.raise_for_status()
            return None
        except Exception as e:
            return f"Teams notification failed: {str(e)}"

    def notify_for_manual_review(self, job_id: str, issue: str) -> str:
        """
        Send notifications about required manual review through configured platforms
        """
        subject = f"Manual Review Required for Job {job_id}"
        body = f"The following issue was detected during ingestion: {issue}\n\nPlease review job {job_id} in the admin interface."

        errors = []

        try:
            # Send email notification
            self.ses_client.send_email(
                Source="noreply@ebookmarketplace.com",
                Destination={"ToAddresses": ["content-team@ebookmarketplace.com"]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": body}}
                }
            )

            # Send platform-specific notifications based on configuration
            if self.platform in [NotificationPlatform.SLACK, NotificationPlatform.BOTH]:
                if error := self._send_slack_notification(subject, body):
                    errors.append(error)

            if self.platform in [NotificationPlatform.TEAMS, NotificationPlatform.BOTH]:
                if error := self._send_teams_notification(subject, body):
                    errors.append(error)

            if errors:
                return f"Partial success. Some notifications failed: {'; '.join(errors)}"
            return "Notification sent successfully"

        except ClientError as e:
            errors.append(f"Email notification failed: {e.response['Error']['Message']}")
            return f"Notification failed: {'; '.join(errors)}"
