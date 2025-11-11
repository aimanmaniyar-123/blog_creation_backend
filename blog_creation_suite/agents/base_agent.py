import asyncio
import json
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from enum import Enum

class AgentStatus(Enum):
    """Agent execution status enumeration"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class BaseAgent(ABC):
    """
    Enhanced Base Agent class for the Blog Creation Suite
    Provides comprehensive functionality for all agent types across all phases
    """

    def __init__(self, name: str, phase: str, description: str = "", dependencies: List[str] = None):
        """
        Initialize BaseAgent with enhanced tracking and configuration

        Args:
            name: Agent name
            phase: Phase this agent belongs to (e.g., "phase1", "phase2")
            description: Brief description of agent functionality
            dependencies: List of agent names this agent depends on
        """
        self.name = name
        self.phase = phase
        self.description = description
        self.dependencies = dependencies or []

        # Status and metrics tracking
        self.status = AgentStatus.IDLE
        self.success_count = 0
        self.failure_count = 0
        self.last_execution_time = 0.0
        self.total_execution_time = 0.0
        self.created_at = datetime.now()
        self.last_run_at = None

        # Configuration and context
        self.config = {}
        self.context = {}
        self.output_cache = None
        self.retry_count = 0
        self.max_retries = 3

        # Setup logging
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main functionality
        Must be implemented by each specific agent

        Args:
            input_data: Input data for the agent

        Returns:
            Dict containing agent results
        """
        pass

    async def pre_execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pre-execution hook for validation and preparation
        Can be overridden by child classes

        Args:
            input_data: Input data to validate

        Returns:
            Processed input data
        """
        # Validate dependencies are met
        if not self.validate_dependencies(input_data):
            raise ValueError(f"Dependencies not met for {self.name}")

        # Log execution start
        self.logger.info(f"Starting execution of {self.name} in {self.phase}")

        return input_data

    async def post_execute(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post-execution hook for cleanup and result processing
        Can be overridden by child classes

        Args:
            result: Execution result to process

        Returns:
            Processed result
        """
        # Cache successful results
        if result.get("status") == "success":
            self.output_cache = result.get("result")

        # Log execution completion
        self.logger.info(f"Completed execution of {self.name}")

        return result

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced run method with comprehensive error handling, retries, and metrics

        Args:
            input_data: Input data for execution

        Returns:
            Standardized result dictionary
        """
        start_time = datetime.now()
        self.status = AgentStatus.RUNNING
        self.last_run_at = start_time

        attempt = 0
        last_error = None

        while attempt <= self.max_retries:
            try:
                # Pre-execution validation and preparation
                processed_input = await self.pre_execute(input_data)

                # Execute main functionality
                result = await self.execute(processed_input)

                # Post-execution processing
                processed_result = await self.post_execute(result)

                # Success metrics
                self.success_count += 1
                self.status = AgentStatus.COMPLETED
                self.retry_count = 0

                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                self.last_execution_time = execution_time
                self.total_execution_time += execution_time

                return {
                    "status": "success",
                    "agent": self.name,
                    "phase": self.phase,
                    "execution_time": execution_time,
                    "attempt": attempt + 1,
                    "result": processed_result,
                    "timestamp": end_time.isoformat()
                }

            except Exception as e:
                attempt += 1
                last_error = e
                self.retry_count = attempt

                self.logger.warning(f"Attempt {attempt} failed for {self.name}: {str(e)}")

                if attempt <= self.max_retries:
                    # Wait before retry with exponential backoff
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    # Max retries exceeded
                    self.failure_count += 1
                    self.status = AgentStatus.ERROR

                    end_time = datetime.now()
                    execution_time = (end_time - start_time).total_seconds()
                    self.last_execution_time = execution_time

                    self.logger.error(f"Max retries exceeded for {self.name}: {str(last_error)}")

                    return {
                        "status": "error",
                        "agent": self.name,
                        "phase": self.phase,
                        "execution_time": execution_time,
                        "attempts": attempt,
                        "error": str(last_error),
                        "error_type": type(last_error).__name__,
                        "result": None,
                        "timestamp": end_time.isoformat()
                    }

        # This should never be reached, but just in case
        self.status = AgentStatus.IDLE
        return {
            "status": "error",
            "agent": self.name,
            "phase": self.phase,
            "error": "Unknown execution error",
            "result": None
        }

    def validate_dependencies(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate that all required dependencies are available in input data

        Args:
            input_data: Input data to check for dependencies

        Returns:
            True if all dependencies are met, False otherwise
        """
        if not self.dependencies:
            return True

        agent_results = input_data.get("agent_results", {})

        for dependency in self.dependencies:
            if dependency not in agent_results:
                self.logger.error(f"Missing dependency: {dependency}")
                return False

        return True

    def get_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive agent statistics and metrics

        Returns:
            Dictionary containing agent statistics
        """
        total_executions = self.success_count + self.failure_count
        success_rate = (self.success_count / total_executions * 100) if total_executions > 0 else 0
        avg_execution_time = (self.total_execution_time / total_executions) if total_executions > 0 else 0

        return {
            "name": self.name,
            "phase": self.phase,
            "description": self.description,
            "status": self.status.value,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": round(success_rate, 2),
            "last_execution_time": self.last_execution_time,
            "average_execution_time": round(avg_execution_time, 3),
            "total_execution_time": round(self.total_execution_time, 3),
            "retry_count": self.retry_count,
            "dependencies": self.dependencies,
            "created_at": self.created_at.isoformat(),
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None
        }

    def reset_stats(self):
        """Reset all statistics and metrics"""
        self.success_count = 0
        self.failure_count = 0
        self.last_execution_time = 0.0
        self.total_execution_time = 0.0
        self.retry_count = 0
        self.status = AgentStatus.IDLE
        self.output_cache = None

    def configure(self, config: Dict[str, Any]):
        """
        Configure agent settings

        Args:
            config: Configuration dictionary
        """
        self.config.update(config)

        # Update max_retries if provided
        if "max_retries" in config:
            self.max_retries = config["max_retries"]

    def set_context(self, context: Dict[str, Any]):
        """
        Set agent execution context

        Args:
            context: Context data for execution
        """
        self.context.update(context)

    def get_cached_output(self) -> Optional[Dict[str, Any]]:
        """
        Get the last successful output from cache

        Returns:
            Cached output or None if no cache exists
        """
        return self.output_cache

    def __str__(self) -> str:
        """String representation of the agent"""
        return f"{self.name} ({self.phase}) - {self.status.value}"

    def __repr__(self) -> str:
        """Detailed string representation of the agent"""
        return f"BaseAgent(name='{self.name}', phase='{self.phase}', status='{self.status.value}')"

# Example usage and template for specific agent implementation:
class ExampleSpecificAgent(BaseAgent):
    """
    Example implementation showing how to extend BaseAgent
    """

    def __init__(self):
        super().__init__(
            name="ExampleAgent",
            phase="phase1", 
            description="Example agent demonstrating BaseAgent usage",
            dependencies=["SomeOtherAgent"]  # Optional dependencies
        )

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement specific agent functionality

        Args:
            input_data: Input data for processing

        Returns:
            Agent-specific results
        """
        # Simulate some work
        await asyncio.sleep(0.1)

        # Process input and generate results
        result = {
            "processed_data": f"Processed: {input_data.get('topic', 'No topic')}",
            "agent_specific_output": "Some specific result",
            "metadata": {
                "processing_time": self.last_execution_time,
                "agent_version": "1.0.0"
            }
        }

        return result

    async def pre_execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optional: Override pre-execution if needed"""
        # Call parent pre-execute
        processed_input = await super().pre_execute(input_data)

        # Add agent-specific pre-processing
        if "topic" not in processed_input:
            processed_input["topic"] = "Default Topic"

        return processed_input
