"""
Metrics Collector

Collects and aggregates pipeline metrics including coverage, quality,
and performance statistics.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from src.modules.docugen.state import FileState


@dataclass
class PipelineMetrics:
    """Aggregated metrics for documentation pipeline."""

    # Coverage metrics
    total_files: int = 0
    layer1_completed: int = 0
    layer2_completed: int = 0
    layer3_completed: int = 0
    fully_documented: int = 0  # All 3 layers complete

    # Quality metrics
    layer1_validation_passed: int = 0
    layer2_validation_passed: int = 0
    layer3_validation_passed: int = 0
    layer1_validation_failed: int = 0
    layer2_validation_failed: int = 0
    layer3_validation_failed: int = 0
    flagged_for_review: int = 0
    errors_encountered: int = 0

    # Refinement metrics
    total_layer1_iterations: int = 0
    total_layer2_iterations: int = 0
    total_layer3_iterations: int = 0
    max_layer1_iterations: int = 0
    max_layer2_iterations: int = 0
    max_layer3_iterations: int = 0

    # Performance metrics
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    total_duration_seconds: float = 0.0
    avg_time_per_file: float = 0.0
    throughput_files_per_hour: float = 0.0

    # Additional metadata
    config_used: Dict[str, Any] = field(default_factory=dict)
    file_details: List[Dict[str, Any]] = field(default_factory=list)


class MetricsCollector:
    """
    Collects and aggregates metrics from the documentation pipeline.

    Tracks coverage, quality, and performance metrics across all processed files.
    """

    def __init__(self):
        """Initialize the MetricsCollector."""
        self.metrics = PipelineMetrics()
        self.file_start_times: Dict[str, datetime] = {}
        self.pipeline_start_time: Optional[datetime] = None

    def start_pipeline(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Mark pipeline start and optionally record configuration.

        Args:
            config: Pipeline configuration dictionary
        """
        self.pipeline_start_time = datetime.now()
        self.metrics.start_time = self.pipeline_start_time.isoformat()

        if config:
            self.metrics.config_used = config

    def end_pipeline(self) -> None:
        """Mark pipeline end and calculate duration metrics."""
        if not self.pipeline_start_time:
            return

        end_time = datetime.now()
        self.metrics.end_time = end_time.isoformat()

        duration = (end_time - self.pipeline_start_time).total_seconds()
        self.metrics.total_duration_seconds = duration

        if self.metrics.total_files > 0:
            self.metrics.avg_time_per_file = duration / self.metrics.total_files
            # Calculate throughput (files per hour)
            if duration > 0:
                self.metrics.throughput_files_per_hour = (self.metrics.total_files / duration) * 3600

    def record_file_start(self, file_path: Path) -> None:
        """
        Record the start time for processing a file.

        Args:
            file_path: Path to the file being processed
        """
        self.file_start_times[str(file_path)] = datetime.now()

    def record_file_completion(self, state: FileState) -> None:
        """
        Record completion of a file and update metrics.

        Args:
            state: Final FileState after processing
        """
        self.metrics.total_files += 1

        # Coverage metrics
        if state.layer1_summary:
            self.metrics.layer1_completed += 1
        if state.layer2_details:
            self.metrics.layer2_completed += 1
        if state.layer3_relationships:
            self.metrics.layer3_completed += 1

        # Check if fully documented (all 3 layers)
        if state.layer1_summary and state.layer2_details and state.layer3_relationships:
            self.metrics.fully_documented += 1

        # Quality metrics - validation results
        if state.layer1_validation:
            if state.layer1_validation.passed:
                self.metrics.layer1_validation_passed += 1
            else:
                self.metrics.layer1_validation_failed += 1

        if state.layer2_validation:
            if state.layer2_validation.passed:
                self.metrics.layer2_validation_passed += 1
            else:
                self.metrics.layer2_validation_failed += 1

        if state.layer3_validation:
            if state.layer3_validation.passed:
                self.metrics.layer3_validation_passed += 1
            else:
                self.metrics.layer3_validation_failed += 1

        # Flags and errors
        if state.flagged_for_review:
            self.metrics.flagged_for_review += 1

        if state.error_message:
            self.metrics.errors_encountered += 1

        # Refinement iterations
        self.metrics.total_layer1_iterations += state.layer1_iterations
        self.metrics.total_layer2_iterations += state.layer2_iterations
        self.metrics.total_layer3_iterations += state.layer3_iterations

        self.metrics.max_layer1_iterations = max(
            self.metrics.max_layer1_iterations, state.layer1_iterations
        )
        self.metrics.max_layer2_iterations = max(
            self.metrics.max_layer2_iterations, state.layer2_iterations
        )
        self.metrics.max_layer3_iterations = max(
            self.metrics.max_layer3_iterations, state.layer3_iterations
        )

        # Calculate file processing time
        file_path_str = str(state.file_path)
        if file_path_str in self.file_start_times:
            start_time = self.file_start_times[file_path_str]
            duration = (datetime.now() - start_time).total_seconds()
        else:
            duration = 0.0

        # Record detailed file info
        file_detail = {
            "file": str(state.file_path),
            "layer1_complete": state.layer1_summary is not None,
            "layer2_complete": state.layer2_details is not None,
            "layer3_complete": state.layer3_relationships is not None,
            "layer1_iterations": state.layer1_iterations,
            "layer2_iterations": state.layer2_iterations,
            "layer3_iterations": state.layer3_iterations,
            "flagged_for_review": state.flagged_for_review,
            "has_error": state.error_message is not None,
            "processing_time_seconds": duration,
        }
        self.metrics.file_details.append(file_detail)

    def get_coverage_percentage(self) -> Dict[str, float]:
        """
        Calculate coverage percentages for each layer.

        Returns:
            Dictionary with coverage percentages
        """
        if self.metrics.total_files == 0:
            return {
                "layer1": 0.0,
                "layer2": 0.0,
                "layer3": 0.0,
                "fully_documented": 0.0,
            }

        return {
            "layer1": (self.metrics.layer1_completed / self.metrics.total_files) * 100,
            "layer2": (self.metrics.layer2_completed / self.metrics.total_files) * 100,
            "layer3": (self.metrics.layer3_completed / self.metrics.total_files) * 100,
            "fully_documented": (self.metrics.fully_documented / self.metrics.total_files) * 100,
        }

    def get_validation_pass_rate(self) -> Dict[str, float]:
        """
        Calculate validation pass rates for each layer.

        Returns:
            Dictionary with pass rate percentages
        """
        def calc_rate(passed: int, failed: int) -> float:
            total = passed + failed
            return (passed / total * 100) if total > 0 else 0.0

        return {
            "layer1": calc_rate(
                self.metrics.layer1_validation_passed,
                self.metrics.layer1_validation_failed
            ),
            "layer2": calc_rate(
                self.metrics.layer2_validation_passed,
                self.metrics.layer2_validation_failed
            ),
            "layer3": calc_rate(
                self.metrics.layer3_validation_passed,
                self.metrics.layer3_validation_failed
            ),
        }

    def get_average_iterations(self) -> Dict[str, float]:
        """
        Calculate average refinement iterations per layer.

        Returns:
            Dictionary with average iterations
        """
        if self.metrics.total_files == 0:
            return {"layer1": 0.0, "layer2": 0.0, "layer3": 0.0}

        return {
            "layer1": self.metrics.total_layer1_iterations / self.metrics.total_files,
            "layer2": self.metrics.total_layer2_iterations / self.metrics.total_files,
            "layer3": self.metrics.total_layer3_iterations / self.metrics.total_files,
        }

    def export_json(self, output_path: Path) -> None:
        """
        Export metrics to JSON file.

        Args:
            output_path: Path where JSON should be written
        """
        metrics_dict = asdict(self.metrics)

        # Add calculated metrics
        metrics_dict["coverage_percentage"] = self.get_coverage_percentage()
        metrics_dict["validation_pass_rate"] = self.get_validation_pass_rate()
        metrics_dict["average_iterations"] = self.get_average_iterations()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metrics_dict, f, indent=2)

    def export_markdown(self, output_path: Path) -> None:
        """
        Export metrics report as markdown.

        Args:
            output_path: Path where markdown should be written
        """
        coverage = self.get_coverage_percentage()
        pass_rates = self.get_validation_pass_rate()
        avg_iterations = self.get_average_iterations()

        lines = [
            "# Documentation Pipeline Metrics Report",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
            f"- **Total Files Processed**: {self.metrics.total_files}",
            f"- **Fully Documented**: {self.metrics.fully_documented} ({coverage['fully_documented']:.1f}%)",
            f"- **Flagged for Review**: {self.metrics.flagged_for_review}",
            f"- **Errors Encountered**: {self.metrics.errors_encountered}",
            "",
            "## Coverage Metrics",
            "",
            f"- **Layer 1 (Summary)**: {self.metrics.layer1_completed}/{self.metrics.total_files} ({coverage['layer1']:.1f}%)",
            f"- **Layer 2 (Details)**: {self.metrics.layer2_completed}/{self.metrics.total_files} ({coverage['layer2']:.1f}%)",
            f"- **Layer 3 (Relationships)**: {self.metrics.layer3_completed}/{self.metrics.total_files} ({coverage['layer3']:.1f}%)",
            "",
            "## Quality Metrics",
            "",
            "### Validation Pass Rates",
            "",
            f"- **Layer 1**: {pass_rates['layer1']:.1f}% ({self.metrics.layer1_validation_passed} passed, {self.metrics.layer1_validation_failed} failed)",
            f"- **Layer 2**: {pass_rates['layer2']:.1f}% ({self.metrics.layer2_validation_passed} passed, {self.metrics.layer2_validation_failed} failed)",
            f"- **Layer 3**: {pass_rates['layer3']:.1f}% ({self.metrics.layer3_validation_passed} passed, {self.metrics.layer3_validation_failed} failed)",
            "",
            "### Refinement Iterations",
            "",
            f"- **Layer 1 Average**: {avg_iterations['layer1']:.2f} (max: {self.metrics.max_layer1_iterations})",
            f"- **Layer 2 Average**: {avg_iterations['layer2']:.2f} (max: {self.metrics.max_layer2_iterations})",
            f"- **Layer 3 Average**: {avg_iterations['layer3']:.2f} (max: {self.metrics.max_layer3_iterations})",
            "",
            "## Performance Metrics",
            "",
            f"- **Start Time**: {self.metrics.start_time or 'N/A'}",
            f"- **End Time**: {self.metrics.end_time or 'N/A'}",
            f"- **Total Duration**: {self.metrics.total_duration_seconds:.2f} seconds",
            f"- **Average Time per File**: {self.metrics.avg_time_per_file:.2f} seconds",
            f"- **Throughput**: {self.metrics.throughput_files_per_hour:.1f} files/hour",
            "",
        ]

        # Add file details table if available
        if self.metrics.file_details:
            lines.extend([
                "## File Details",
                "",
                "| File | L1 | L2 | L3 | Iterations (L1/L2/L3) | Time (s) | Status |",
                "|------|----|----|----|-----------------------|----------|--------|",
            ])

            for detail in self.metrics.file_details:
                l1 = "✅" if detail["layer1_complete"] else "❌"
                l2 = "✅" if detail["layer2_complete"] else "❌"
                l3 = "✅" if detail["layer3_complete"] else "❌"
                iterations = f"{detail['layer1_iterations']}/{detail['layer2_iterations']}/{detail['layer3_iterations']}"
                time_str = f"{detail['processing_time_seconds']:.2f}"

                status = "✅"
                if detail["flagged_for_review"]:
                    status = "⚠️"
                if detail["has_error"]:
                    status = "❌"

                file_name = Path(detail["file"]).name
                lines.append(f"| {file_name} | {l1} | {l2} | {l3} | {iterations} | {time_str} | {status} |")

            lines.append("")

        content = "\n".join(lines)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
