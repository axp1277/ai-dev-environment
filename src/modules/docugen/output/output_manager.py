"""
Output File Manager

Manages file writing, directory structure mirroring, and index generation
for the documentation output.
"""

import os
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger


class OutputManager:
    """
    Manages output file operations for generated documentation.

    Handles directory structure creation, atomic file writes,
    and index generation for navigation.
    """

    def __init__(self, base_output_dir: Path, source_root: Optional[Path] = None):
        """
        Initialize the OutputManager.

        Args:
            base_output_dir: Root directory for documentation output
            source_root: Root directory of source codebase (for mirroring structure)
        """
        self.base_output_dir = Path(base_output_dir)
        self.source_root = Path(source_root) if source_root else None
        self.generated_files: List[Dict[str, str]] = []

    def ensure_output_directory(self) -> None:
        """
        Create output directory if it doesn't exist.

        Sets appropriate permissions (750) for security.
        """
        self.base_output_dir.mkdir(parents=True, exist_ok=True)

        # Set restrictive permissions on Unix-like systems
        try:
            os.chmod(self.base_output_dir, 0o750)
        except (OSError, NotImplementedError):
            # Windows or permission errors - log but continue
            logger.debug(f"Could not set permissions on {self.base_output_dir}")

    def get_output_path(self, source_file: Path) -> Path:
        """
        Get the output path for a source file, mirroring directory structure.

        Args:
            source_file: Path to the source file

        Returns:
            Path where the documentation should be written
        """
        # Convert source file to .md extension
        md_filename = source_file.stem + ".md"

        if self.source_root:
            # Mirror directory structure relative to source root
            try:
                relative_path = source_file.relative_to(self.source_root)
                output_path = self.base_output_dir / relative_path.parent / md_filename
            except ValueError:
                # File is not relative to source_root, use flat structure
                logger.warning(f"File {source_file} not under {self.source_root}, using flat structure")
                output_path = self.base_output_dir / md_filename
        else:
            # Flat structure if no source root specified
            output_path = self.base_output_dir / md_filename

        return output_path

    def write_documentation(self, source_file: Path, content: str) -> Path:
        """
        Write documentation to file using atomic write operation.

        Args:
            source_file: Original source file path
            content: Markdown content to write

        Returns:
            Path to the written documentation file

        Raises:
            IOError: If file write fails
        """
        output_path = self.get_output_path(source_file)

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic write: write to temp file, then rename
        try:
            # Create temp file in same directory for atomic rename
            temp_fd, temp_path = tempfile.mkstemp(
                dir=output_path.parent,
                prefix=".tmp_",
                suffix=".md"
            )

            try:
                # Write content to temp file
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Atomic rename
                os.replace(temp_path, output_path)

                logger.info(f"Wrote documentation: {output_path}")

                # Track generated file
                self.generated_files.append({
                    "source": str(source_file),
                    "output": str(output_path),
                    "timestamp": datetime.now().isoformat()
                })

                return output_path

            except Exception:
                # Clean up temp file on error
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass
                raise

        except Exception as e:
            logger.error(f"Failed to write documentation for {source_file}: {e}")
            raise IOError(f"Failed to write {output_path}: {e}") from e

    def generate_index(self, title: str = "Documentation Index") -> Path:
        """
        Generate an index file linking all generated documentation.

        Args:
            title: Title for the index page

        Returns:
            Path to the generated index file
        """
        # Ensure output directory exists
        self.ensure_output_directory()

        index_path = self.base_output_dir / "INDEX.md"

        lines = [
            f"# {title}",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"Total Files: {len(self.generated_files)}",
            "",
            "## Files",
            "",
        ]

        # Group files by directory if using mirrored structure
        if self.source_root:
            # Group by directory
            files_by_dir: Dict[str, List[Dict[str, str]]] = {}
            for file_info in sorted(self.generated_files, key=lambda x: x["output"]):
                output_path = Path(file_info["output"])
                relative_to_base = output_path.relative_to(self.base_output_dir)
                dir_name = str(relative_to_base.parent) if relative_to_base.parent != Path('.') else "Root"

                if dir_name not in files_by_dir:
                    files_by_dir[dir_name] = []
                files_by_dir[dir_name].append(file_info)

            # Generate directory sections
            for dir_name in sorted(files_by_dir.keys()):
                lines.append(f"### {dir_name}")
                lines.append("")

                for file_info in files_by_dir[dir_name]:
                    output_path = Path(file_info["output"])
                    relative_link = output_path.relative_to(self.base_output_dir)
                    source_name = Path(file_info["source"]).name
                    lines.append(f"- [{source_name}]({relative_link})")

                lines.append("")
        else:
            # Flat list
            for file_info in sorted(self.generated_files, key=lambda x: x["source"]):
                source_name = Path(file_info["source"]).name
                output_name = Path(file_info["output"]).name
                lines.append(f"- [{source_name}]({output_name})")

        lines.append("")
        content = "\n".join(lines)

        # Write index file
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Generated index: {index_path}")
            return index_path

        except Exception as e:
            logger.error(f"Failed to generate index: {e}")
            raise IOError(f"Failed to write index {index_path}: {e}") from e

    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about generated documentation.

        Returns:
            Dictionary with statistics (total_files, total_size_bytes, etc.)
        """
        total_size = 0
        for file_info in self.generated_files:
            output_path = Path(file_info["output"])
            if output_path.exists():
                total_size += output_path.stat().st_size

        return {
            "total_files": len(self.generated_files),
            "total_size_bytes": total_size,
            "output_directory": str(self.base_output_dir),
        }

    def clear_output_directory(self) -> None:
        """
        Clear all markdown files from output directory.

        WARNING: This deletes all .md files in the output directory.
        """
        if not self.base_output_dir.exists():
            return

        deleted_count = 0
        for md_file in self.base_output_dir.rglob("*.md"):
            try:
                md_file.unlink()
                deleted_count += 1
            except OSError as e:
                logger.warning(f"Failed to delete {md_file}: {e}")

        logger.info(f"Cleared {deleted_count} markdown files from {self.base_output_dir}")
        self.generated_files.clear()
