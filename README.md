# Blog Post Writer using Multi-agents AI System

- Multi-agents AI System을 이용한 블로그 글 작성 툴

---

# Getting Started

## Prerequisites

- poetry
- virtualenv (pyenv, python 3.10)

### Install Dependencies

```bash
$ poetry shell
$ poetry install --no-root
```

## Execution Program

- `topic`과 `filename`을 아래와 같이 입력해서 글을 생성할 수 있습니다.
- 생성된 글의 예시는 [Introduction of Multi-agents AI System like CrewAI](./resources/introduction-of-multi-agents-ai-system-like-crewai.md)에서 확인하실 수 있습니다.

```bash
$ python main.py --topic="Introduction of Multi-Agents AI System like CrewAI (https://www.crewai.com/)" --filename=./resources/introduction-of-multi-agents-ai-system-like-crewai.md

Searching data from github: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.53it/s]
[DEBUG]: Working Agent: Senior Content Planner
[INFO]: Starting Task:
1. "Introduction of Multi-Agents AI System like CrewAI (https://www.crewai.com/)"과 관련한 최근 기술 블로그 내용들을 우선시하십시오. **Medium(https://medium.com)블로그에 게시된 내용을 우선해야 함**
2. 소개, 주요 포인트, 관련된 자료(데이터 혹은 코드)를 포함하는 자세한 콘텐츠 개요를 작성해줘.
3. SEO 키워드와 관련된 데이터 또는 소스 및 코드를 포함하십시오.


> Entering new CrewAgentExecutor chain...
2024-06-09 22:31:10,335 - 140704737011456 - manager.py-manager:282 - WARNING: Error in TokenCalcHandler.on_llm_start callback: KeyError('Could not automatically map gpt-4o to a tokeniser. Please use `tiktoken.get_encoding` to explicitly get the tokeniser you expect.')
우선, 주어진 주제인 'Introduction of Multi-Agents AI System like CrewAI'와 관련된 정보를 수집하고, 이를 바탕으로 콘텐츠 계획을 세우기 위해 필요한 도구들을 활용하겠습니다.

먼저, CrewAI와 관련된 최신 정보를 Medium 블로그에서 우선적으로 찾아보겠습니다.

Action: Search the internet
Action Input: {"search_query": "Introduction of Multi-Agents AI System CrewAI site:medium.com"}



Search results: Title: Create a Blog Writer Multi-Agent System using Crewai and ...
Link: https://medium.com/the-ai-forum/create-a-blog-writer-multi-agent-system-using-crewai-and-ollama-f47654a5e1cd
Snippet: CrewAi is a cutting-edge framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI ...
...
---
```