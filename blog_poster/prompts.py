from datetime import datetime

from pytz import timezone

from blog_poster.utils import Tone


def auto_agent_instructions():
    return """
        이 작업은 주어진 주제에 대해 조사하는 것으로, 주제의 복잡성이나 명확한 답변의 유무에 관계없이 수행됩니다. 조사는 해당 분야와 주제를 연구하는 데 사용할 수 있는 특정 서버에 의해 수행됩니다. 에이전트는 그들의 전문 분야에 따라 분류되며, 각 서버 유형은 대응하는 이모지와 연결됩니다.
        example:
        task: "애플 주식에 투자해야 할까요?"
        response:
        {
            "server": "💰 재무 에이전트",
            "agent_role_prompt": "당신은 경험이 풍부한 재무 분석 AI 어시스턴트입니다. 주요 목표는 제공된 데이터와 트렌드를 기반으로 포괄적이고, 통찰력 있으며, 공정하고 체계적으로 정리된 금융 보고서를 작성하는 것입니다."
        }
        task: "스니커즈 재판매가 수익성이 있을까요?"
        response:
        {
            "server": "📈 비즈니스 분석 에이전트",
            "agent_role_prompt": "당신은 경험이 풍부한 AI 비즈니스 분석 어시스턴트입니다. 주요 목표는 제공된 비즈니스 데이터, 시장 동향 및 전략 분석을 기반으로 포괄적이고, 통찰력 있으며, 공정하고 체계적으로 정리된 비즈니스 보고서를 작성하는 것입니다."
        }
        task: "텔아비브에서 가장 흥미로운 명소는 무엇인가요?"
        response:
        {
            "server: "🌍 여행 에이전트",
            "agent_role_prompt": "당신은 세계를 여행한 경험이 풍부한 AI 여행 가이드 어시스턴트입니다. 주요 목적은 주어진 위치에 대한 역사, 명소 및 문화적 통찰력을 포함한 흥미롭고, 통찰력 있으며, 공정하고 체계적으로 정리된 여행 보고서를 작성하는 것입니다."
        }
    """


def generate_search_queries_prompt(
    query: str,
    parent_query: str,
    max_sub_queries: int = 3,
):
    if parent_query:
        task = f"{parent_query} - {query}"
    else:
        task = query

    return (
        f'다음 작업에서 객관적인 의견을 형성하기 위해 {max_sub_queries}개의 구글 검색 쿼리를 작성하십시오: "{task}"'
        f'필요한 경우 현재 날짜를 사용하십시오: {datetime.now(timezone("Asia/Seoul")).strftime("%Y%m%d")}.\n'
        f"또한, 쿼리에는 위치, 이름 등 작업 세부 사항을 포함해야 합니다.\n"
        f'응답은 다음 형식의 문자열 목록이어야 합니다: ["쿼리 1", "쿼리 2", "쿼리 3"].\n'
        f"응답은 오직 목록만 포함해야 합니다."
    )


def generate_subtopics_prompt() -> str:
    return """
    제공된 main topic:

    {task}

    그리고 research data:

    {data}

    - 작업에 대해 생성될 보고서 문서의 헤더를 나타내는 하위 주제 목록을 작성하십시오.
    - 가능한 하위 주제 목록은 다음과 같습니다: {subtopics}.
    - 중복된 하위 주제가 없어야 합니다.
    - 하위 주제의 수는 최대 {max_subtopics}로 제한해야 합니다.
    - 마지막으로 하위 주제를 작업에 따라 관련 있고 의미 있는 순서로 정렬하여 상세한 보고서에 제시할 수 있어야 합니다.

    "중요!":
    - 모든 하위 주제는 주요 주제와 제공된 연구 데이터에만 관련이 있어야 합니다!

    {format_instructions}
"""


def generate_report_introduction(question: str, research_summary: str = "") -> str:
    return f"""{research_summary}\n
위의 최신 정보를 사용하여 주제 -- {question}에 대한 상세 보고서 소개를 준비하십시오.
- 소개는 간결하고, 잘 구조화되며, 정보가 풍부해야 합니다. Markdown 문법을 사용하십시오.
- 이 소개는 더 큰 보고서의 일부가 될 것이므로, 일반적으로 보고서에 포함되는 다른 섹션은 포함하지 마십시오.
- 소개는 적절한 주제를 가진 H1 제목이 앞에 있어야 합니다.
- 필요한 경우 문장과 관련된 하이퍼링크를 Markdown 문법([url website](url))으로 포함해야 합니다.
필요할 경우 현재 날짜는 {datetime.now(timezone("Asia/Seoul")).strftime('%Y%m%d')}로 가정하십시오.
"""


def generate_subtopic_report_prompt(
    current_subtopic,
    existing_headers: list,
    main_topic: str,
    context,
    report_format: str = "apa",
    max_subsections=5,
    total_words=800,
    tone: Tone = Tone.Objective.value,
) -> str:
    return f"""
"Context":
"{context}"

"Main Topic and Subtopic":
최신 정보를 사용하여 주요 주제: {main_topic} 아래의 하위 주제: {current_subtopic}에 대한 상세 보고서를 작성하십시오.
하위 섹션의 수는 최대 {max_subsections}개로 제한해야 합니다.

"Content Focus":

- 보고서는 질문에 답하는 데 초점을 맞추어야 하며, 잘 구조화되고, 정보가 풍부하고, 깊이 있으며, 가능하면 사실과 숫자를 포함해야 합니다.
- Markdown 문법을 사용하고 {report_format.upper()} 형식을 따르십시오.

"Structure and Formatting":
- 이 하위 보고서는 더 큰 보고서의 일부가 될 것이므로, 소개나 결론 섹션 없이 적절한 하위 주제로 나누어진 본문만 포함하십시오.
- 보고서에서 참조된 관련 출처 URL에 Markdown 하이퍼링크를 반드시 포함해야 합니다. 예를 들어:

  # Report Header
  이것은 샘플 텍스트입니다. ([url website](url))

"Existing Subtopic Reports":
- 이것은 기존 하위 주제 보고서와 그 섹션 헤더 목록입니다:

  {existing_headers}.

- 중복을 피하기 위해 위의 헤더나 관련 세부 정보를 사용하지 마십시오. 더 큰 보고서의 헤딩으로 사용할 가장 큰 헤더(H1)를 피하고, 콘텐츠 구조를 위해 더 작은 Markdown 헤더(H2 또는 H3)를 사용하십시오.

"날짜":
필요할 경우 현재 날짜는 {datetime.now(timezone("Asia/Seoul")).strftime('%Y%m%d')}로 가정하십시오.

"!IMPORTANT":
- 주요 주제에 초점을 맞춰야 합니다! 관련 없는 정보는 반드시 제외하십시오!
- 소개, 결론, 요약 또는 참고 문헌 섹션이 없어야 합니다.
- 보고서에서 참조된 관련 문장에 Markdown 문법([url website](url))을 사용하여 하이퍼링크를 반드시 포함하십시오.
- 보고서의 길이는 최소 {total_words} 단어 이상이어야 합니다.
- 보고서 전반에 걸쳐 {tone.value} 어조를 사용하십시오.
"""
