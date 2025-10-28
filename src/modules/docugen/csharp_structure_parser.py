"""
C# Structure Parser

This module provides functionality to parse C# files and extract their structure,
including classes, attributes (fields/properties), and methods.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
import tree_sitter_c_sharp as tscsharp
from tree_sitter import Language, Parser, Node


@dataclass
class MethodInfo:
    """Represents a method in a C# class."""
    name: str
    return_type: str
    parameters: List[str]
    modifiers: List[str]
    line_number: int
    is_constructor: bool = False


@dataclass
class AttributeInfo:
    """Represents a field or property in a C# class."""
    name: str
    type: str
    modifiers: List[str]
    line_number: int
    is_property: bool = False


@dataclass
class ClassInfo:
    """Represents a C# class with its attributes and methods."""
    name: str
    namespace: Optional[str]
    modifiers: List[str]
    base_classes: List[str]
    line_number: int
    attributes: List[AttributeInfo] = field(default_factory=list)
    methods: List[MethodInfo] = field(default_factory=list)
    nested_classes: List['ClassInfo'] = field(default_factory=list)


class CSharpStructureParser:
    """Parser for extracting structure from C# files."""
    
    def __init__(self):
        """Initialize the parser with C# language support."""
        self.language = Language(tscsharp.language())
        self.parser = Parser(self.language)
    
    def parse_file(self, file_path: str) -> List[ClassInfo]:
        """
        Parse a C# file and extract all class structures.
        
        Args:
            file_path: Path to the C# file
            
        Returns:
            List of ClassInfo objects representing all classes in the file
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        return self.parse_source(source_code)
    
    def parse_source(self, source_code: str) -> List[ClassInfo]:
        """
        Parse C# source code and extract all class structures.
        
        Args:
            source_code: C# source code as a string
            
        Returns:
            List of ClassInfo objects representing all classes in the source
        """
        tree = self.parser.parse(bytes(source_code, 'utf8'))
        root_node = tree.root_node
        
        # Find the namespace(s) and classes
        classes = []
        namespace = self._extract_namespace(root_node)
        
        # Find all class declarations
        self._find_classes(root_node, namespace, classes)
        
        return classes
    
    def _extract_namespace(self, node: Node) -> Optional[str]:
        """Extract the namespace from the syntax tree."""
        namespace_nodes = self._find_nodes_by_type(node, 'namespace_declaration')
        if namespace_nodes:
            # Get the first namespace declaration
            name_node = self._find_child_by_field(namespace_nodes[0], 'name')
            if name_node:
                return self._get_node_text(name_node)
        return None
    
    def _find_classes(self, node: Node, namespace: Optional[str], classes: List[ClassInfo], parent_class: Optional[ClassInfo] = None):
        """Recursively find all class declarations in the syntax tree."""
        if node.type == 'class_declaration':
            class_info = self._parse_class(node, namespace)
            if parent_class:
                parent_class.nested_classes.append(class_info)
            else:
                classes.append(class_info)
            
            # Look for nested classes
            body_node = self._find_child_by_field(node, 'body')
            if body_node:
                for child in body_node.children:
                    self._find_classes(child, namespace, classes, class_info)
        else:
            # Continue searching in children
            for child in node.children:
                self._find_classes(child, namespace, classes, parent_class)
    
    def _parse_class(self, node: Node, namespace: Optional[str]) -> ClassInfo:
        """Parse a class declaration node."""
        name_node = self._find_child_by_field(node, 'name')
        class_name = self._get_node_text(name_node) if name_node else 'Unknown'
        
        # Extract modifiers
        modifiers = self._extract_modifiers(node)
        
        # Extract base classes/interfaces
        base_classes = self._extract_base_list(node)
        
        # Create class info
        class_info = ClassInfo(
            name=class_name,
            namespace=namespace,
            modifiers=modifiers,
            base_classes=base_classes,
            line_number=node.start_point[0] + 1
        )
        
        # Parse the class body
        body_node = self._find_child_by_field(node, 'body')
        if body_node:
            self._parse_class_body(body_node, class_info)
        
        return class_info
    
    def _parse_class_body(self, body_node: Node, class_info: ClassInfo):
        """Parse the body of a class to extract attributes and methods."""
        for child in body_node.children:
            if child.type == 'field_declaration':
                attributes = self._parse_field(child)
                class_info.attributes.extend(attributes)
            elif child.type == 'property_declaration':
                attribute = self._parse_property(child)
                if attribute:
                    class_info.attributes.append(attribute)
            elif child.type == 'method_declaration':
                method = self._parse_method(child)
                if method:
                    class_info.methods.append(method)
            elif child.type == 'constructor_declaration':
                method = self._parse_constructor(child)
                if method:
                    class_info.methods.append(method)
    
    def _parse_field(self, node: Node) -> List[AttributeInfo]:
        """Parse a field declaration (can have multiple variables)."""
        attributes = []
        
        modifiers = self._extract_modifiers(node)
        
        # Get type
        type_node = self._find_child_by_type(node, 'variable_declaration')
        field_type = 'unknown'
        if type_node:
            type_child = self._find_child_by_field(type_node, 'type')
            if type_child:
                field_type = self._get_node_text(type_child)
            
            # Get all variable declarators
            declarators = self._find_nodes_by_type(type_node, 'variable_declarator')
            for declarator in declarators:
                name_node = self._find_child_by_field(declarator, 'name')
                if name_node:
                    attribute = AttributeInfo(
                        name=self._get_node_text(name_node),
                        type=field_type,
                        modifiers=modifiers,
                        line_number=node.start_point[0] + 1,
                        is_property=False
                    )
                    attributes.append(attribute)
        
        return attributes
    
    def _parse_property(self, node: Node) -> Optional[AttributeInfo]:
        """Parse a property declaration."""
        modifiers = self._extract_modifiers(node)
        
        # Get type
        type_node = self._find_child_by_field(node, 'type')
        prop_type = self._get_node_text(type_node) if type_node else 'unknown'
        
        # Get name
        name_node = self._find_child_by_field(node, 'name')
        if not name_node:
            return None
        
        return AttributeInfo(
            name=self._get_node_text(name_node),
            type=prop_type,
            modifiers=modifiers,
            line_number=node.start_point[0] + 1,
            is_property=True
        )
    
    def _parse_method(self, node: Node) -> Optional[MethodInfo]:
        """Parse a method declaration."""
        modifiers = self._extract_modifiers(node)
        
        # Get return type
        type_node = self._find_child_by_field(node, 'type')
        return_type = self._get_node_text(type_node) if type_node else 'void'
        
        # Get name
        name_node = self._find_child_by_field(node, 'name')
        if not name_node:
            return None
        
        method_name = self._get_node_text(name_node)
        
        # Get parameters
        parameters = self._extract_parameters(node)
        
        return MethodInfo(
            name=method_name,
            return_type=return_type,
            parameters=parameters,
            modifiers=modifiers,
            line_number=node.start_point[0] + 1,
            is_constructor=False
        )
    
    def _parse_constructor(self, node: Node) -> Optional[MethodInfo]:
        """Parse a constructor declaration."""
        modifiers = self._extract_modifiers(node)
        
        # Get name
        name_node = self._find_child_by_field(node, 'name')
        if not name_node:
            return None
        
        constructor_name = self._get_node_text(name_node)
        
        # Get parameters
        parameters = self._extract_parameters(node)
        
        return MethodInfo(
            name=constructor_name,
            return_type='',  # Constructors don't have return types
            parameters=parameters,
            modifiers=modifiers,
            line_number=node.start_point[0] + 1,
            is_constructor=True
        )
    
    def _extract_modifiers(self, node: Node) -> List[str]:
        """Extract access modifiers and other modifiers from a declaration."""
        modifiers = []
        modifier_types = ['public', 'private', 'protected', 'internal', 'static', 
                         'virtual', 'override', 'abstract', 'sealed', 'readonly', 
                         'const', 'async', 'extern', 'partial']
        
        for child in node.children:
            if child.type in modifier_types:
                modifiers.append(child.type)
        
        return modifiers
    
    def _extract_base_list(self, node: Node) -> List[str]:
        """Extract base classes and interfaces."""
        base_classes = []
        base_list_node = self._find_child_by_field(node, 'bases')
        
        if base_list_node:
            for child in base_list_node.children:
                if child.type == 'base_type':
                    type_node = self._find_child_by_field(child, 'type')
                    if type_node:
                        base_classes.append(self._get_node_text(type_node))
        
        return base_classes
    
    def _extract_parameters(self, node: Node) -> List[str]:
        """Extract method parameters."""
        parameters = []
        param_list_node = self._find_child_by_field(node, 'parameters')
        
        if param_list_node:
            for child in param_list_node.children:
                if child.type == 'parameter':
                    param_text = self._get_node_text(child)
                    parameters.append(param_text)
        
        return parameters
    
    def _find_child_by_field(self, node: Node, field_name: str) -> Optional[Node]:
        """Find a child node by field name."""
        return node.child_by_field_name(field_name)
    
    def _find_child_by_type(self, node: Node, node_type: str) -> Optional[Node]:
        """Find the first child node of a specific type."""
        for child in node.children:
            if child.type == node_type:
                return child
        return None
    
    def _find_nodes_by_type(self, node: Node, node_type: str) -> List[Node]:
        """Find all descendant nodes of a specific type."""
        results = []
        
        def traverse(n: Node):
            if n.type == node_type:
                results.append(n)
            for child in n.children:
                traverse(child)
        
        traverse(node)
        return results
    
    def _get_node_text(self, node: Node) -> str:
        """Get the text content of a node."""
        return node.text.decode('utf8')


def print_class_tree(class_info: ClassInfo, indent: int = 0):
    """
    Pretty print a class structure as a tree.
    
    Args:
        class_info: The class to print
        indent: Current indentation level
    """
    prefix = "  " * indent
    modifiers_str = " ".join(class_info.modifiers)
    base_str = f" : {', '.join(class_info.base_classes)}" if class_info.base_classes else ""
    
    print(f"{prefix}Class: {modifiers_str} {class_info.name}{base_str} (line {class_info.line_number})")
    
    if class_info.namespace:
        print(f"{prefix}  Namespace: {class_info.namespace}")
    
    if class_info.attributes:
        print(f"{prefix}  Attributes:")
        for attr in class_info.attributes:
            attr_type = "Property" if attr.is_property else "Field"
            mods = " ".join(attr.modifiers) if attr.modifiers else "default"
            print(f"{prefix}    [{attr_type}] {mods} {attr.type} {attr.name} (line {attr.line_number})")
    
    if class_info.methods:
        print(f"{prefix}  Methods:")
        for method in class_info.methods:
            mods = " ".join(method.modifiers) if method.modifiers else "default"
            params = ", ".join(method.parameters) if method.parameters else ""
            method_type = "Constructor" if method.is_constructor else "Method"
            ret_type = "" if method.is_constructor else f"{method.return_type} "
            print(f"{prefix}    [{method_type}] {mods} {ret_type}{method.name}({params}) (line {method.line_number})")
    
    if class_info.nested_classes:
        print(f"{prefix}  Nested Classes:")
        for nested in class_info.nested_classes:
            print_class_tree(nested, indent + 2)


def class_to_dict(class_info: ClassInfo) -> Dict[str, Any]:
    """
    Convert a ClassInfo object to a dictionary for JSON serialization.
    
    Args:
        class_info: The class to convert
        
    Returns:
        Dictionary representation of the class structure
    """
    return {
        "name": class_info.name,
        "namespace": class_info.namespace,
        "modifiers": class_info.modifiers,
        "base_classes": class_info.base_classes,
        "line_number": class_info.line_number,
        "attributes": [
            {
                "name": attr.name,
                "type": attr.type,
                "modifiers": attr.modifiers,
                "line_number": attr.line_number,
                "is_property": attr.is_property
            }
            for attr in class_info.attributes
        ],
        "methods": [
            {
                "name": method.name,
                "return_type": method.return_type,
                "parameters": method.parameters,
                "modifiers": method.modifiers,
                "line_number": method.line_number,
                "is_constructor": method.is_constructor
            }
            for method in class_info.methods
        ],
        "nested_classes": [class_to_dict(nested) for nested in class_info.nested_classes]
    }


def main():
    """CLI entry point for C# structure parser."""
    import click
    import sys
    import json as json_lib
    from pathlib import Path
    
    @click.command()
    @click.argument('path', type=click.Path(exists=True))
    @click.option('--json', '-j', 'json_output', type=str, default=None, 
                  help='Output as JSON. Optionally specify output file path (otherwise prints to stdout)')
    @click.option('--output', '-o', 'output_file', type=str, default=None,
                  help='Output file path (alternative to -j with filename)')
    def parse_csharp(path, json_output, output_file):
        """Parse C# file(s) and display their structure.
        
        PATH: Path to a C# file or directory containing C# files
        
        If a directory is provided, it will recursively search for .cs files
        and output results in JSON format.
        """
        try:
            parser = CSharpStructureParser()
            path_obj = Path(path)
            
            # Determine output mode and file
            use_json = json_output is not None or output_file is not None or path_obj.is_dir()
            out_file = json_output if json_output else output_file
            
            # Check if it's a file or directory
            if path_obj.is_file():
                # Single file mode
                classes = parser.parse_file(str(path_obj))
                
                if not classes:
                    click.echo("No classes found in the file.", err=True)
                    sys.exit(1)
                
                if use_json:
                    # Output as JSON
                    output = [class_to_dict(class_info) for class_info in classes]
                    json_str = json_lib.dumps(output, indent=2)
                    
                    if out_file:
                        with open(out_file, 'w', encoding='utf-8') as f:
                            f.write(json_str)
                        click.echo(f"Output written to: {out_file}", err=True)
                    else:
                        click.echo(json_str)
                else:
                    # Output as tree view
                    click.echo("=" * 80)
                    click.echo(f"C# Structure Analysis: {path}")
                    click.echo("=" * 80)
                    click.echo()
                    
                    for class_info in classes:
                        print_class_tree(class_info)
                        click.echo()
            
            elif path_obj.is_dir():
                # Directory mode - always output as JSON
                click.echo(f"Scanning directory: {path}", err=True)
                
                # Find all .cs files recursively
                cs_files = list(path_obj.rglob("*.cs"))
                
                if not cs_files:
                    click.echo("No .cs files found in directory.", err=True)
                    sys.exit(1)
                
                click.echo(f"Found {len(cs_files)} C# files", err=True)
                
                # Parse all files and collect results
                results = {}
                total_classes = 0
                errors = []
                
                for cs_file in cs_files:
                    try:
                        classes = parser.parse_file(str(cs_file))
                        if classes:
                            # Store relative path as key
                            relative_path = str(cs_file.relative_to(path_obj))
                            results[relative_path] = [class_to_dict(c) for c in classes]
                            total_classes += len(classes)
                    except Exception as e:
                        errors.append({
                            "file": str(cs_file.relative_to(path_obj)),
                            "error": str(e)
                        })
                
                # Output results as JSON
                output = {
                    "directory": str(path_obj),
                    "total_files": len(cs_files),
                    "total_classes": total_classes,
                    "files": results
                }
                
                if errors:
                    output["errors"] = errors
                
                json_str = json_lib.dumps(output, indent=2)
                
                # If no output file specified, create default output path
                if not out_file:
                    # Get the last directory name from the input path
                    dir_name = path_obj.name
                    # Create output directory structure: output/{dir_name}/
                    output_dir = Path("output") / dir_name
                    output_dir.mkdir(parents=True, exist_ok=True)
                    # Create output file: output/{dir_name}/{dir_name_lowercase}.json
                    out_file = str(output_dir / f"{dir_name.lower()}.json")
                
                if out_file:
                    with open(out_file, 'w', encoding='utf-8') as f:
                        f.write(json_str)
                    click.echo(f"Output written to: {out_file}", err=True)
                    click.echo(f"Parsed {total_classes} classes from {len(cs_files)} files", err=True)
                else:
                    click.echo(json_str)
                
                if errors:
                    click.echo(f"\nWarning: {len(errors)} files had parsing errors", err=True)
            
            else:
                click.echo(f"Invalid path: {path}", err=True)
                sys.exit(1)
        
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
    
    parse_csharp()


# Example usage
if __name__ == "__main__":
    main()
