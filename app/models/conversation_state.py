from dataclasses import dataclass, field


@dataclass
class ConversationState:

    # Hiring context

    role: str | None = None

    seniority: str | None = None

    domain: str | None = None 

    skills: list[str] = field(default_factory=list)

    job_description: bool = False

    # Intent flags

    wants_comparison: bool = False

    wants_refinement: bool = False

    wants_recommendation: bool = False

    off_topic: bool = False

    # Utility

    latest_message: str = ""