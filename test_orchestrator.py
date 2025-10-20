"""
Quick test of the DocuGenOrchestrator with the sample codebase.
"""

from pathlib import Path
from src.modules.docugen.orchestrator import create_orchestrator
from src.modules.docugen.state import GraphConfig

def main():
    # Configure the orchestrator
    config = GraphConfig(
        summarizer_model="qwen3:1.7b",
        detailing_model="granite3.3:latest",
        relationship_model="qwen3:1.7b",
        max_iterations=3
    )

    # Create orchestrator
    orchestrator = create_orchestrator(config)

    # Test with a single file
    test_file = Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/HttpService.cs")

    print(f"\n{'='*80}")
    print(f"Testing Orchestrator with: {test_file.name}")
    print(f"{'='*80}\n")

    # Process the file
    result = orchestrator.process_file(test_file)

    # Display results
    print(f"\n{'='*80}")
    print("RESULTS")
    print(f"{'='*80}\n")

    print(f"File: {result.file_path.name}")
    print(f"Flagged for Review: {result.flagged_for_review}")
    print(f"Error: {result.error_message or 'None'}")
    print()

    if result.layer1_summary:
        print("✅ Layer 1 Complete:")
        print(f"  Summary: {result.layer1_summary.summary[:100]}...")
        print(f"  Category: {result.layer1_summary.category}")
        print(f"  Iterations: {result.layer1_iterations}")
        print(f"  Validation: {'Passed' if result.layer1_validation and result.layer1_validation.passed else 'Failed'}")

    if result.layer2_details:
        print("\n✅ Layer 2 Complete:")
        print(f"  Classes: {len(result.layer2_details.classes)}")
        print(f"  Standalone Methods: {len(result.layer2_details.standalone_methods)}")
        print(f"  Iterations: {result.layer2_iterations}")
        print(f"  Validation: {'Passed' if result.layer2_validation and result.layer2_validation.passed else 'Failed'}")

    if result.layer3_relationships:
        print("\n✅ Layer 3 Complete:")
        print(f"  Architectural Role: {result.layer3_relationships.architectural_role}")
        print(f"  Dependencies: {len(result.layer3_relationships.dependencies)}")
        print(f"  Dependents: {len(result.layer3_relationships.dependents)}")
        print(f"  Iterations: {result.layer3_iterations}")
        print(f"  Validation: {'Passed' if result.layer3_validation and result.layer3_validation.passed else 'Failed'}")

    print(f"\n{'='*80}")
    print("Pipeline Complete!")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
