from django.db.models import TextChoices


class CompetitionStage(TextChoices):
    COMPLETED = 'COMPLETED'
    FINAL = 'FINAL'
    SEMI_FINAL = 'SEMI_FINAL'
    QUARTER_FINAL = 'QUARTER_FINAL'
    LAST_16 = 'LAST_16'
    LAST_32 = 'LAST_32'
