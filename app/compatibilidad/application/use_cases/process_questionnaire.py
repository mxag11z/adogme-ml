from ...domain.entities.user_answer_entity import UserAnswerEntity


class ProcessQuestionnaire:
    """Receives questionnaire answers, computes and returns user_vector."""

    def execute(self, answers: UserAnswerEntity) -> list[float]:
        return answers.to_vector()
