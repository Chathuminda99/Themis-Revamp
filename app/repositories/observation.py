import uuid
from sqlalchemy.orm import Session
from app.models.project import ProjectObservation
from app.repositories.base import BaseRepository


class ProjectObservationRepository(BaseRepository[ProjectObservation]):
    """Repository for ProjectObservation model."""

    model = ProjectObservation

    def __init__(self, db: Session):
        super().__init__(db)

    def get_for_control(
        self, project_id: uuid.UUID, control_id: uuid.UUID
    ) -> list[ProjectObservation]:
        """Get all observations for a specific control in a project."""
        return (
            self.db.query(ProjectObservation)
            .filter(
                ProjectObservation.project_id == project_id,
                ProjectObservation.framework_control_id == control_id,
            )
            .all()
        )

    def create_observation(
        self,
        project_id: uuid.UUID,
        control_id: uuid.UUID,
        observation_text: str,
        recommendation_text: str,
    ) -> ProjectObservation:
        """Create a new observation."""
        observation = ProjectObservation(
            id=uuid.uuid4(),
            project_id=project_id,
            framework_control_id=control_id,
            observation_text=observation_text,
            recommendation_text=recommendation_text,
        )
        self.db.add(observation)
        self.db.commit()
        return observation

    def delete_observation(self, observation_id: uuid.UUID) -> bool:
        """Delete an observation and its evidence files."""
        observation = self.db.query(ProjectObservation).filter(
            ProjectObservation.id == observation_id
        ).first()
        if observation:
            self.db.delete(observation)
            self.db.commit()
            return True
        return False
