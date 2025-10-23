"""Tests for project planner"""

import pytest
from unittest.mock import Mock, AsyncMock
from devonika.planner.project_planner import ProjectPlanner


@pytest.fixture
def mock_llm():
    """Mock LLM interface"""
    llm = Mock()
    llm.generate = AsyncMock()
    return llm


@pytest.fixture
def mock_logger():
    """Mock logger"""
    return Mock()


@pytest.fixture
def planner(mock_llm, mock_logger):
    """Create planner instance"""
    return ProjectPlanner(mock_llm, mock_logger)


@pytest.mark.asyncio
async def test_create_comprehensive_plan(planner, mock_llm):
    """Test creating a comprehensive project plan"""
    # Mock LLM responses
    mock_llm.generate.return_value = '{"core_functionality": ["feature1", "feature2"]}'

    description = "Create a simple TODO app"
    plan = await planner.create_comprehensive_plan(description)

    assert plan is not None
    assert "description" in plan
    assert plan["description"] == description
    assert "components" in plan
    assert "tasks" in plan


@pytest.mark.asyncio
async def test_generate_project_name(planner, mock_llm):
    """Test project name generation"""
    mock_llm.generate.return_value = "todo_app"

    project_plan = {"description": "A simple TODO app"}
    name = await planner.generate_project_name(project_plan)

    assert name == "todo_app"
    assert "_" in name or name.islower()
