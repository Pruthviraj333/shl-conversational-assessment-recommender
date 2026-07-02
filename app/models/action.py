from enum import Enum


class AgentAction(str, Enum):

    CLARIFY = "clarify"

    RECOMMEND = "recommend"

    REFINE = "refine"

    COMPARE = "compare"

    REFUSE = "refuse"