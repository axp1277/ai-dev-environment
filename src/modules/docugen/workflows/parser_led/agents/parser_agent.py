"""
Parser Agent - Layer 0 (Structure Harvest Node)

Discovers C# files and extracts structural information using Tree-sitter.
This agent provides ground truth for the documentation pipeline.

Responsibilities:
- Recursively discover all .cs files in directory
- Parse each file with Tree-sitter to extract structure
- Store StructureSnapshot for each file
- Handle parsing errors gracefully
- Track progress with detailed logging
"""

from pathlib import Path
from typing import List
from loguru import logger

from ..state import ParserLedState, FileDiscoveryResult
from ....shared.parsers.csharp_structure_parser import (
    CSharpStructureParser,
    StructureSnapshot
)


def discover_csharp_files(directory_path: str) -> FileDiscoveryResult:
    """
    Recursively discover all C# files in the directory.

    Args:
        directory_path: Root directory to search

    Returns:
        FileDiscoveryResult with discovered files
    """
    path = Path(directory_path)

    if not path.exists():
        logger.error(f"Directory does not exist: {directory_path}")
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    if not path.is_dir():
        logger.error(f"Path is not a directory: {directory_path}")
        raise NotADirectoryError(f"Not a directory: {directory_path}")

    # Discover .cs files
    cs_files = list(path.rglob("*.cs"))
    cs_file_paths = [str(f.relative_to(path)) for f in cs_files]

    # Discover .csproj files (for future dependency extraction)
    csproj_files = list(path.rglob("*.csproj"))
    csproj_file_paths = [str(f.relative_to(path)) for f in csproj_files]

    logger.info(
        f"Discovered {len(cs_files)} C# files and {len(csproj_files)} .csproj files",
        directory=directory_path,
        cs_count=len(cs_files),
        csproj_count=len(csproj_files)
    )

    return FileDiscoveryResult(
        total_files=len(cs_files),
        cs_files=cs_file_paths,
        csproj_files=csproj_file_paths
    )


def parse_csharp_file(
    file_path: str,
    base_directory: str,
    parser: CSharpStructureParser,
    include_private: bool = True
) -> StructureSnapshot:
    """
    Parse a single C# file and extract its structure.

    Args:
        file_path: Relative path to the C# file
        base_directory: Base directory for resolving relative paths
        parser: CSharpStructureParser instance
        include_private: Whether to include private members

    Returns:
        StructureSnapshot containing parsed structure

    Raises:
        Exception: If parsing fails
    """
    full_path = Path(base_directory) / file_path

    logger.debug(f"Parsing file: {file_path}")

    try:
        snapshot = parser.parse_file(str(full_path))

        # Log summary
        logger.info(
            f"Parsed {file_path}",
            file=file_path,
            classes=len(snapshot.classes),
            namespace=snapshot.namespace
        )

        return snapshot

    except Exception as e:
        logger.error(
            f"Failed to parse {file_path}: {e}",
            file=file_path,
            error=str(e)
        )
        raise


def parser_agent_node(state: ParserLedState) -> ParserLedState:
    """
    Parser Agent LangGraph Node - Layer 0 (Structure Harvest).

    Discovers all C# files in the directory and parses them to extract
    structural information. This provides ground truth for documentation.

    Args:
        state: Current workflow state

    Returns:
        Updated state with structure_snapshots populated
    """
    logger.info(
        "Starting Parser Agent (Structure Harvest)",
        directory=state.directory_path,
        include_private=state.config.include_private_members
    )

    # Step 1: Discover files
    try:
        discovery_result = discover_csharp_files(state.directory_path)
        state.discovered_files = discovery_result.cs_files

        if not discovery_result.cs_files:
            logger.warning(f"No C# files found in {state.directory_path}")
            return state

    except Exception as e:
        logger.error(f"File discovery failed: {e}")
        raise

    # Step 2: Parse each file
    parser = CSharpStructureParser()
    total_files = len(state.discovered_files)

    for idx, file_path in enumerate(state.discovered_files, start=1):
        try:
            logger.info(
                f"Processing file {idx}/{total_files}",
                file=file_path,
                progress=f"{idx}/{total_files}"
            )

            # Parse the file
            snapshot = parse_csharp_file(
                file_path=file_path,
                base_directory=state.directory_path,
                parser=parser,
                include_private=state.config.include_private_members
            )

            # Store snapshot in state
            state.structure_snapshots[file_path] = snapshot

            # Log class summary
            for class_info in snapshot.classes:
                logger.debug(
                    f"  Found class: {class_info.name}",
                    class_name=class_info.name,
                    is_partial=class_info.is_partial,
                    is_nested=class_info.is_nested,
                    methods=len(class_info.methods),
                    properties=len(class_info.properties),
                    fields=len(class_info.attributes)
                )

        except Exception as e:
            # Store error but continue processing other files
            error_msg = f"Parsing error: {str(e)}"
            state.parsing_errors[file_path] = error_msg
            logger.error(
                f"Failed to parse {file_path}, continuing with remaining files",
                file=file_path,
                error=error_msg
            )

    # Step 3: Log summary
    successful_count = len(state.structure_snapshots)
    error_count = len(state.parsing_errors)
    total_classes = sum(len(s.classes) for s in state.structure_snapshots.values())

    logger.info(
        "Parser Agent complete",
        successful_files=successful_count,
        failed_files=error_count,
        total_classes=total_classes,
        success_rate=f"{successful_count / total_files * 100:.1f}%" if total_files > 0 else "0%"
    )

    if error_count > 0:
        logger.warning(
            f"Parsing failed for {error_count} files",
            failed_files=list(state.parsing_errors.keys())
        )

    return state


# Export for LangGraph graph construction
__all__ = [
    "parser_agent_node",
    "discover_csharp_files",
    "parse_csharp_file"
]
