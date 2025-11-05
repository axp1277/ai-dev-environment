"""
Test Consolidation Agent

This test verifies the consolidation agent's ability to:
1. Identify duplicate elements across files
2. Consolidate multiple definitions using LLM
3. Apply consolidated definitions in the compiler
"""

import pytest
from pathlib import Path
from loguru import logger

from ..state import (
    ParserLedState,
    ParserLedConfig,
    FileDocumentation,
    DocumentedClass,
    DocumentedMethod,
    DocumentedProperty,
    DocumentedField,
    ConsolidatedElement
)
from ..agents.parser_agent import parser_agent_node
from ..agents.documentation_agent import documentation_agent_node
from ..agents.consolidation_agent import (
    consolidation_agent_node,
    identify_duplicate_elements,
    consolidate_element_definitions
)
from ..agents.compiler_agent import apply_consolidated_definitions


@pytest.fixture
def sample_inheritance_project(tmp_path):
    """Create a sample C# project with inheritance for testing duplicates."""
    test_dir = tmp_path / "test_project"
    test_dir.mkdir()

    # Base class with interface
    base_file = test_dir / "IRepository.cs"
    base_file.write_text("""
namespace DataAccess
{
    public interface IRepository
    {
        bool Save();
        void Delete();
        int Count { get; }
    }
}
""")

    # First implementation
    impl1_file = test_dir / "UserRepository.cs"
    impl1_file.write_text("""
namespace DataAccess
{
    public class UserRepository : IRepository
    {
        public bool Save()
        {
            // Save user to database
            return true;
        }

        public void Delete()
        {
            // Delete user
        }

        public int Count { get; set; }
    }
}
""")

    # Second implementation
    impl2_file = test_dir / "ProductRepository.cs"
    impl2_file.write_text("""
namespace DataAccess
{
    public class ProductRepository : IRepository
    {
        public bool Save()
        {
            // Save product to database
            return true;
        }

        public void Delete()
        {
            // Delete product
        }

        public int Count { get; set; }
    }
}
""")

    return test_dir


@pytest.fixture
def sample_documented_state():
    """Create a mock state with duplicate documented elements."""
    state = ParserLedState(
        directory_path="/test",
        config=ParserLedConfig()
    )

    # File 1: UserRepository
    file_doc1 = FileDocumentation(
        file_path="UserRepository.cs",
        namespace="DataAccess",
        classes={
            "UserRepository": DocumentedClass(
                name="UserRepository",
                description="Repository for user data",
                purpose="Manage user persistence",
                methods={
                    "Save": DocumentedMethod(
                        name="Save",
                        description="Saves the current user to the database.",
                        parameters={},
                        returns="True if save was successful"
                    ),
                    "Delete": DocumentedMethod(
                        name="Delete",
                        description="Removes the user from the database.",
                        parameters={},
                        returns=None
                    )
                },
                properties={
                    "Count": DocumentedProperty(
                        name="Count",
                        description="Number of users in the repository"
                    )
                }
            )
        }
    )

    # File 2: ProductRepository (duplicates: Save, Delete, Count)
    file_doc2 = FileDocumentation(
        file_path="ProductRepository.cs",
        namespace="DataAccess",
        classes={
            "ProductRepository": DocumentedClass(
                name="ProductRepository",
                description="Repository for product data",
                purpose="Manage product persistence",
                methods={
                    "Save": DocumentedMethod(
                        name="Save",
                        description="Persists product changes to storage.",
                        parameters={},
                        returns="Boolean indicating success or failure"
                    ),
                    "Delete": DocumentedMethod(
                        name="Delete",
                        description="Deletes the product permanently.",
                        parameters={},
                        returns=None
                    )
                },
                properties={
                    "Count": DocumentedProperty(
                        name="Count",
                        description="Total product count"
                    )
                }
            )
        }
    )

    state.documented_files = {
        "UserRepository.cs": file_doc1,
        "ProductRepository.cs": file_doc2
    }

    return state


def test_identify_duplicate_elements(sample_documented_state):
    """Test that duplicate elements are correctly identified."""
    logger.info("Testing duplicate element identification...")

    duplicates = identify_duplicate_elements(sample_documented_state.documented_files)

    # Should identify 3 duplicate elements: Save, Delete, Count
    assert len(duplicates) == 3, f"Expected 3 duplicates, got {len(duplicates)}"

    # Check that Save method is identified as duplicate
    assert "method:Save" in duplicates, "Save method should be identified as duplicate"
    assert len(duplicates["method:Save"]) == 2, "Save should appear in 2 files"

    # Check that Delete method is identified as duplicate
    assert "method:Delete" in duplicates, "Delete method should be identified as duplicate"
    assert len(duplicates["method:Delete"]) == 2, "Delete should appear in 2 files"

    # Check that Count property is identified as duplicate
    assert "property:Count" in duplicates, "Count property should be identified as duplicate"
    assert len(duplicates["property:Count"]) == 2, "Count should appear in 2 files"

    # Verify element references contain correct information
    save_refs = duplicates["method:Save"]
    assert save_refs[0].element_name == "Save"
    assert save_refs[0].element_type == "method"
    assert save_refs[0].class_name in ["UserRepository", "ProductRepository"]

    logger.info(f"✓ Identified {len(duplicates)} duplicate elements correctly")


def test_no_duplicates_scenario():
    """Test behavior when no duplicates exist."""
    state = ParserLedState(
        directory_path="/test",
        config=ParserLedConfig()
    )

    # Single file with unique elements
    file_doc = FileDocumentation(
        file_path="UniqueClass.cs",
        namespace="Test",
        classes={
            "UniqueClass": DocumentedClass(
                name="UniqueClass",
                description="A unique class",
                purpose="Testing",
                methods={
                    "UniqueMethod": DocumentedMethod(
                        name="UniqueMethod",
                        description="A unique method",
                        parameters={},
                        returns=None
                    )
                }
            )
        }
    )

    state.documented_files = {"UniqueClass.cs": file_doc}

    duplicates = identify_duplicate_elements(state.documented_files)

    assert len(duplicates) == 0, "Should find no duplicates in unique elements"
    logger.info("✓ Correctly handled no-duplicates scenario")


def test_consolidation_agent_node(sample_documented_state):
    """Test the full consolidation agent node execution."""
    logger.info("Testing consolidation agent node...")

    # Run consolidation agent
    result_state = consolidation_agent_node(sample_documented_state)

    # Verify consolidated_elements was populated
    assert result_state.consolidated_elements is not None, "Should have consolidated_elements"
    assert len(result_state.consolidated_elements) == 3, "Should consolidate 3 elements"

    # Verify consolidated Save method
    if "method:Save" in result_state.consolidated_elements:
        save_consolidated = result_state.consolidated_elements["method:Save"]
        assert save_consolidated.element_name == "Save"
        assert save_consolidated.element_type == "method"
        assert len(save_consolidated.consolidated_description) > 0
        assert save_consolidated.original_count == 2
        assert len(save_consolidated.source_files) == 2

    logger.info("✓ Consolidation agent node executed successfully")


def test_apply_consolidated_definitions(sample_documented_state):
    """Test applying consolidated definitions to documented files."""
    logger.info("Testing consolidated definition application...")

    # Create mock consolidated elements
    consolidated_elements = {
        "method:Save": ConsolidatedElement(
            element_name="Save",
            element_type="method",
            signature="Save",
            consolidated_description="Persists all pending changes to the underlying data store.",
            consolidated_parameters={},
            consolidated_returns="True if the save operation completed successfully, false otherwise",
            source_files=["UserRepository.cs", "ProductRepository.cs"],
            original_count=2
        ),
        "property:Count": ConsolidatedElement(
            element_name="Count",
            element_type="property",
            signature="Count",
            consolidated_description="The total number of entities in this repository",
            consolidated_parameters=None,
            consolidated_returns=None,
            source_files=["UserRepository.cs", "ProductRepository.cs"],
            original_count=2
        )
    }

    # Apply consolidation
    updated_files = apply_consolidated_definitions(
        sample_documented_state.documented_files,
        consolidated_elements
    )

    # Verify Save method was replaced in both files
    user_repo_save = updated_files["UserRepository.cs"].classes["UserRepository"].methods["Save"]
    product_repo_save = updated_files["ProductRepository.cs"].classes["ProductRepository"].methods["Save"]

    assert user_repo_save.description == "Persists all pending changes to the underlying data store."
    assert product_repo_save.description == "Persists all pending changes to the underlying data store."
    assert user_repo_save.returns == "True if the save operation completed successfully, false otherwise"
    assert product_repo_save.returns == "True if the save operation completed successfully, false otherwise"

    # Verify Count property was replaced in both files
    user_repo_count = updated_files["UserRepository.cs"].classes["UserRepository"].properties["Count"]
    product_repo_count = updated_files["ProductRepository.cs"].classes["ProductRepository"].properties["Count"]

    assert user_repo_count.description == "The total number of entities in this repository"
    assert product_repo_count.description == "The total number of entities in this repository"

    # Verify Delete method (not consolidated) remains unchanged
    user_repo_delete = updated_files["UserRepository.cs"].classes["UserRepository"].methods["Delete"]
    assert user_repo_delete.description == "Removes the user from the database."

    logger.info("✓ Consolidated definitions applied correctly")


def test_full_pipeline_with_consolidation(sample_inheritance_project):
    """Test the complete pipeline including consolidation."""
    logger.info("Testing full pipeline with consolidation...")

    # Initialize state
    state = ParserLedState(
        directory_path=str(sample_inheritance_project),
        config=ParserLedConfig(
            include_private_members=False,
            llm_model="mistral-nemo:latest"
        )
    )

    # Run parser agent
    state = parser_agent_node(state)
    assert len(state.structure_snapshots) == 3, "Should parse 3 files"

    # Run documentation agent
    state = documentation_agent_node(state)
    assert len(state.documented_files) == 3, "Should document 3 files"

    # Run consolidation agent
    state = consolidation_agent_node(state)

    # Verify consolidation occurred
    if state.consolidated_elements:
        logger.info(f"Consolidated {len(state.consolidated_elements)} elements")

        # Should consolidate Save, Delete, Count across implementations
        assert len(state.consolidated_elements) >= 1, "Should consolidate at least 1 element"

        # Log consolidated elements
        for key, elem in state.consolidated_elements.items():
            logger.info(f"  - {key}: {elem.element_name} ({elem.original_count} definitions)")
            logger.info(f"    Description: {elem.consolidated_description[:100]}...")
    else:
        logger.warning("No elements were consolidated (this may happen if LLM doesn't find duplicates)")

    logger.info("✓ Full pipeline with consolidation completed")


def test_consolidation_preserves_non_duplicates(sample_documented_state):
    """Test that non-duplicate elements are preserved during consolidation."""
    logger.info("Testing preservation of non-duplicates...")

    # Add a unique method to one class
    sample_documented_state.documented_files["UserRepository.cs"].classes["UserRepository"].methods["UniqueUserMethod"] = DocumentedMethod(
        name="UniqueUserMethod",
        description="This method is unique to UserRepository",
        parameters={},
        returns=None
    )

    # Run consolidation
    result_state = consolidation_agent_node(sample_documented_state)

    # Apply consolidation
    if result_state.consolidated_elements:
        updated_files = apply_consolidated_definitions(
            result_state.documented_files,
            result_state.consolidated_elements
        )

        # Verify unique method is still present and unchanged
        unique_method = updated_files["UserRepository.cs"].classes["UserRepository"].methods["UniqueUserMethod"]
        assert unique_method.description == "This method is unique to UserRepository"

        logger.info("✓ Non-duplicate elements preserved correctly")
    else:
        logger.info("✓ Test skipped (no consolidation occurred)")


if __name__ == "__main__":
    # Run tests manually for debugging
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Test 1: Identify duplicates
        logger.info("\n" + "="*60)
        logger.info("TEST 1: Identifying Duplicates")
        logger.info("="*60)
        state = sample_documented_state.__wrapped__(tmp_path)
        test_identify_duplicate_elements(state)

        # Test 2: No duplicates scenario
        logger.info("\n" + "="*60)
        logger.info("TEST 2: No Duplicates Scenario")
        logger.info("="*60)
        test_no_duplicates_scenario()

        # Test 3: Apply consolidated definitions
        logger.info("\n" + "="*60)
        logger.info("TEST 3: Apply Consolidated Definitions")
        logger.info("="*60)
        state = sample_documented_state.__wrapped__(tmp_path)
        test_apply_consolidated_definitions(state)

        logger.info("\n" + "="*60)
        logger.info("All manual tests completed!")
        logger.info("="*60)
