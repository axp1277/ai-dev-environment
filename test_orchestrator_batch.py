"""
Test DocuGenOrchestrator with multiple files (batch processing).
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

    # Test with directory (limit to 2 files for quick test)
    test_dir = Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services")

    print(f"\n{'='*80}")
    print(f"Testing Orchestrator with directory: {test_dir.name}")
    print(f"{'='*80}\n")

    # Process the directory
    results = orchestrator.process_directory(test_dir, pattern="*.cs")

    # Display summary
    print(f"\n{'='*80}")
    print("BATCH PROCESSING RESULTS")
    print(f"{'='*80}\n")

    print(f"Total files processed: {len(results)}")

    completed = sum(1 for s in results.values() if not s.flagged_for_review and not s.error_message)
    flagged = sum(1 for s in results.values() if s.flagged_for_review)
    errors = sum(1 for s in results.values() if s.error_message)

    print(f"✅ Completed successfully: {completed}")
    print(f"⚠️  Flagged for review: {flagged}")
    print(f"❌ Errors: {errors}")

    print(f"\n{'='*80}")
    print("Individual File Results:")
    print(f"{'='*80}\n")

    for file_path, state in results.items():
        print(f"📄 {file_path.name}")
        print(f"   Layer 1: {'✅ Passed' if state.layer1_validation and state.layer1_validation.passed else '❌ Failed'}")
        print(f"   Layer 2: {'✅ Passed' if state.layer2_validation and state.layer2_validation.passed else '❌ Failed'}")
        print(f"   Layer 3: {'✅ Passed' if state.layer3_validation and state.layer3_validation.passed else '❌ Failed'}")
        print(f"   Status: {'⚠️ Flagged' if state.flagged_for_review else '✅ Complete'}")
        print()

    print(f"{'='*80}")
    print("Batch Pipeline Complete!")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
