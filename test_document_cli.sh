#!/bin/bash
# Test the document CLI command on a small subset

# Create a temp directory with just 2 files for quick testing
mkdir -p /tmp/docugen_test
cp data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/HttpService.cs /tmp/docugen_test/
cp data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/WorkerPool.cs /tmp/docugen_test/

echo "Testing document command on 2 files..."
uv run python -m src.modules.docugen.cli document -c config.yaml -i /tmp/docugen_test

# Cleanup
rm -rf /tmp/docugen_test
