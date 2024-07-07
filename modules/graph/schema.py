from typing import TypedDict, Dict, List


class BlogTaskGraphState(TypedDict):
    """
    state to store results
    """

    topic: str

    # results
    research: str
    introduction: str
    main_text: str
    conclusion: str
    code: str

    #
    references: List[Dict]
    edited_contents: List[Dict]
