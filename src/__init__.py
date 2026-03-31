"""
Proposal Builder - AI-Powered RFP Response Tool
"""

__version__ = "2.0.0"

from data_models import (
    ProjectStructure,
    Workstream,
    Module,
    Activity,
    DependencyGraph,
    Evidence,
    AgentReasoning,
    OptimizationResult,
    ExportConfig
)

from rag_engine import RAGEngine
from agents import (
    WorkstreamAgent,
    DependencyAgent,
    ModuleAgent,
    TimelineOptimizer
)

from utils import (
    save_project,
    load_project,
    list_saved_projects,
    print_project_summary,
    calculate_project_metrics,
    validate_environment
)

from visualizations import ProjectVisualizer

from exports import (
    ExcelExporter,
    PowerPointExporter,
    export_project
)

__all__ = [
    # Data Models
    'ProjectStructure',
    'Workstream',
    'Module',
    'Activity',
    'DependencyGraph',
    'Evidence',
    'AgentReasoning',
    'OptimizationResult',
    'ExportConfig',

    # Core Components
    'RAGEngine',
    'WorkstreamAgent',
    'DependencyAgent',
    'ModuleAgent',
    'TimelineOptimizer',

    # Utilities
    'save_project',
    'load_project',
    'list_saved_projects',
    'print_project_summary',
    'calculate_project_metrics',
    'validate_environment',

    # Visualizations
    'ProjectVisualizer',

    # Exports
    'ExcelExporter',
    'PowerPointExporter',
    'export_project',
]
