from crewai import Task, Agent
from textwrap import dedent


def create_task(
    agent: Agent,
    description: str,
    expected_output: str,
    async_execution: bool = False,
    output_file: str = None,
) -> Task:

    task = Task(
        agent=agent,
        description=dedent(description),
        expected_output=dedent(expected_output),
        async_execution=async_execution,
        output_file=output_file,
    )
    return task
