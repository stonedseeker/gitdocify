"""
Documentation generator using OpenAI API
"""

import json
import logging
from typing import Dict, Any, List
import tiktoken
from openai import OpenAI

logger = logging.getLogger(__name__)

class DocumentationGenerator:
    """Generates documentation using OpenAI API."""
    
    def __init__(self, api_key: str, model: str = 'gpt-4'):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.total_tokens = 0
        
        # Initialize tokenizer
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def generate_documentation(self, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive documentation from codebase analysis."""
        
        # Generate different sections
        sections = []
        
        # Project Overview
        sections.append(self._generate_overview(analysis))
        
        # Architecture
        sections.append(self._generate_architecture(analysis))
        
        # Installation & Setup
        sections.append(self._generate_installation(analysis))
        
        # Usage
        sections.append(self._generate_usage(analysis))
        
        # API Reference
        sections.append(self._generate_api_reference(analysis))
        
        # Configuration
        sections.append(self._generate_configuration(analysis))
        
        # Development
        sections.append(self._generate_development(analysis))
        
        # Join all sections
        documentation = '\n\n'.join(filter(None, sections))
        
        return documentation
    
    def _generate_overview(self, analysis: Dict[str, Any]) -> str:
        """Generate project overview section."""
        project_info = analysis['project_info']
        
        # Format the data properly for the prompt
        languages_str = json.dumps(project_info['languages'], indent=2)
        structure_str = json.dumps(analysis['structure'], indent=2)
        dependencies_str = json.dumps(analysis['dependencies'], indent=2)
        readme_content = analysis['readme'] or 'No existing README found'
        
        prompt = f"""
        Generate a comprehensive project overview/README for this codebase:
        
        Project Name: {project_info['name']}
        Total Files: {project_info['total_files']}
        Total Lines: {project_info['total_lines']}
        Languages: {languages_str}
        
        Directory Structure:
        {structure_str}
        
        Dependencies:
        {dependencies_str}
        
        Existing README:
        {readme_content}
        
        Generate a markdown document with:
        1. Project title and description
        2. Key features
        3. Tech stack
        4. Quick start guide
        5. Project structure explanation
        
        Make it professional, clear, and engaging. Use proper markdown formatting.
        """
        
        return self._call_openai(prompt, "Generate project overview")
    
    def _generate_architecture(self, analysis: Dict[str, Any]) -> str:
        """Generate architecture documentation."""
        
        # Get key files for architecture analysis
        key_files = self._get_key_files(analysis['files'])
        
        if not key_files:
            return ""
        
        files_summary = []
        for file_info in key_files[:10]:  # Limit to prevent token overflow
            files_summary.append({
                'path': file_info['path'],
                'language': file_info['language'],
                'type': file_info.get('type', 'unknown'),
                'classes': file_info.get('classes', []),
                'functions': file_info.get('functions', []),
                'imports': file_info.get('imports', [])[:10]  # Limit imports
            })
        
        structure_str = json.dumps(analysis['structure'], indent=2)
        files_str = json.dumps(files_summary, indent=2)
        
        prompt = f"""
        Analyze the architecture of this codebase and generate documentation:
        
        Project Structure:
        {structure_str}
        
        Key Files Analysis:
        {files_str}
        
        Generate a markdown section titled "## Architecture" that includes:
        1. High-level architecture overview
        2. Main components and their responsibilities
        3. Data flow
        4. Design patterns used
        5. Module relationships
        
        Be technical but accessible. Use diagrams in text form where helpful.
        """
        
        return self._call_openai(prompt, "Generate architecture documentation")
    
    def _generate_installation(self, analysis: Dict[str, Any]) -> str:
        """Generate installation and setup documentation."""
        
        dependencies = analysis['dependencies']
        config_files = analysis['config_files']
        
        dependencies_str = json.dumps(dependencies, indent=2)
        config_files_str = json.dumps([{'name': cf['name'], 'path': cf['path']} for cf in config_files], indent=2)
        
        prompt = f"""
        Generate installation and setup documentation for this project:
        
        Dependencies:
        {dependencies_str}
        
        Configuration Files:
        {config_files_str}
        
        Generate a markdown section titled "## Installation & Setup" that includes:
        1. Prerequisites
        2. Installation steps
        3. Environment setup
        4. Configuration requirements
        5. Verification steps
        
        Provide clear, step-by-step instructions.
        """
        
        return self._call_openai(prompt, "Generate installation documentation")
    
    def _generate_usage(self, analysis: Dict[str, Any]) -> str:
        """Generate usage documentation."""
        
        # Find main entry points
        main_files = [f for f in analysis['files'] if 'main' in f['name'].lower() or 'app' in f['name'].lower()]
        
        if not main_files:
            main_files = analysis['files'][:3]  # Take first few files
        
        main_files_data = []
        for f in main_files:
            main_files_data.append({
                'path': f['path'],
                'name': f['name'],
                'language': f['language'],
                'functions': f.get('functions', [])[:5],
                'classes': f.get('classes', [])[:5]
            })
        
        main_files_str = json.dumps(main_files_data, indent=2)
        
        prompt = f"""
        Generate usage documentation for this project:
        
        Main Files:
        {main_files_str}
        
        Generate a markdown section titled "## Usage" that includes:
        1. Basic usage examples
        2. Common use cases
        3. Code examples
        4. Command-line usage (if applicable)
        5. Important notes
        
        Provide practical, runnable examples.
        """
        
        return self._call_openai(prompt, "Generate usage documentation")
    
    def _generate_api_reference(self, analysis: Dict[str, Any]) -> str:
        """Generate API reference documentation."""
        
        # Get files with classes and functions
        api_files = [f for f in analysis['files'] 
                    if f.get('classes') or f.get('functions')]
        
        if not api_files:
            return ""
        
        # Limit to prevent token overflow
        api_summary = []
        for file_info in api_files[:5]:
            api_summary.append({
                'path': file_info['path'],
                'language': file_info['language'],
                'classes': file_info.get('classes', []),
                'functions': file_info.get('functions', [])
            })
        
        api_summary_str = json.dumps(api_summary, indent=2)
        
        prompt = f"""
        Generate API reference documentation for this codebase:
        
        API Files:
        {api_summary_str}
        
        Generate a markdown section titled "## API Reference" that includes:
        1. Main classes and their methods
        2. Public functions and their parameters
        3. Return types and descriptions
        4. Usage examples for key APIs
        5. Error handling
        
        Focus on public APIs that users would interact with.
        """
        
        return self._call_openai(prompt, "Generate API reference")
    
    def _generate_configuration(self, analysis: Dict[str, Any]) -> str:
        """Generate configuration documentation."""
        
        config_files = analysis['config_files']
        
        if not config_files:
            return ""
        
        config_data = []
        for cf in config_files:
            config_data.append({
                'name': cf['name'],
                'path': cf['path'],
                'content_preview': cf['content'][:500]  # First 500 chars
            })
        
        config_str = json.dumps(config_data, indent=2)
        
        prompt = f"""
        Generate configuration documentation for this project:
        
        Configuration Files:
        {config_str}
        
        Generate a markdown section titled "## Configuration" that includes:
        1. Available configuration options
        2. Configuration file formats
        3. Environment variables
        4. Default values
        5. Configuration examples
        
        Explain what each configuration option does.
        """
        
        return self._call_openai(prompt, "Generate configuration documentation")
    
    def _generate_development(self, analysis: Dict[str, Any]) -> str:
        """Generate development documentation."""
        
        test_files = [f for f in analysis['files'] if f.get('type') == 'test']
        
        structure_str = json.dumps(analysis['structure'], indent=2)
        dependencies_str = json.dumps(analysis['dependencies'], indent=2)
        
        prompt = f"""
        Generate development documentation for this project:
        
        Project Structure:
        {structure_str}
        
        Test Files Found: {len(test_files)}
        Dependencies: {dependencies_str}
        
        Generate a markdown section titled "## Development" that includes:
        1. Development setup
        2. Code structure and conventions
        3. Testing approach
        4. Contributing guidelines
        5. Build and deployment process
        
        Focus on helping developers contribute to the project.
        """
        
        return self._call_openai(prompt, "Generate development documentation")
    
    def _get_key_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify key files for architecture analysis."""
        
        key_files = []
        
        # Priority order
        priorities = [
            lambda f: 'main' in f['name'].lower(),
            lambda f: 'app' in f['name'].lower(),
            lambda f: 'server' in f['name'].lower(),
            lambda f: 'client' in f['name'].lower(),
            lambda f: 'api' in f['name'].lower(),
            lambda f: 'model' in f['name'].lower(),
            lambda f: 'controller' in f['name'].lower(),
            lambda f: 'service' in f['name'].lower(),
            lambda f: f.get('classes', []),
            lambda f: f.get('functions', []),
        ]
        
        for priority_func in priorities:
            matching_files = [f for f in files if priority_func(f)]
            key_files.extend(matching_files)
            
            # Remove duplicates while preserving order
            seen = set()
            key_files = [f for f in key_files if f['path'] not in seen and not seen.add(f['path'])]
        
        return key_files
    
    def _call_openai(self, prompt: str, description: str) -> str:
        """Make API call to OpenAI."""
        
        try:
            logger.info(f"Generating: {description}")
            
            # Count tokens in prompt
            tokens = len(self.tokenizer.encode(prompt))
            logger.info(f"Prompt tokens: {tokens}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical documentation expert. Generate clear, comprehensive, and well-structured documentation in markdown format. Be thorough but concise."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            self.total_tokens += response.usage.total_tokens
            
            logger.info(f"Generated {description} ({response.usage.total_tokens} tokens)")
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating {description}: {e}")
            return f"## {description}\n\nError generating this section: {e}"