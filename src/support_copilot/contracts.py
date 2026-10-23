from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TicketCategory(StrEnum):
    WITHDRAWAL = "withdrawal"
    OTHER = "other"


class TicketUrgency(StrEnum):
    HIGH = "high"
    NORMAL = "normal"


class TicketLanguage(StrEnum):
    ENGLISH = "en"
    UNKNOWN = "unknown"


class TicketSentiment(StrEnum):
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class SupportTicket(ContractModel):
    ticket_id: str = Field(min_length=1)
    text: str = Field(min_length=1)


class ProcessingResult(ContractModel):
    ticket_id: str = Field(min_length=1)
    category: TicketCategory
    urgency: TicketUrgency
    language: TicketLanguage
    sentiment: TicketSentiment
