import os
import sys
import click
from dotenv import load_dotenv
from pathlib import Path

from .analyzer import CodebaseAnalyzer
from .generator import DocumentationGenerator
from .utils import setup_logging, validate_openai_key

# Load environment variables
load_dotenv()

@click.command()
@click.option('--path', '-p', default='.', help='Path to the codebase (default: current directory)')
@click.option('--output', '-o', default='DOCUMENTATION.md', help='Output file name (default: DOCUMENTATION.md)')
@click.option('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
@click.option('--model', default='gpt-4', help='OpenAI model to use (default: gpt-4)')
@click.option('--exclude', multiple=True, help='Patterns to exclude (can be used multiple times)')
@click.option('--include-tests', is_flag=True, help='Include test files in analysis')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def generate_docs(path, output, api_key, model, exclude, include_tests, verbose):
    """Generate comprehensive documentation for your codebase using AI."""
    
    # Setup logging
    setup_logging(verbose)
    
    # Validate API key
    api_key = api_key or os.getenv('OPENAI_API_KEY')
    if not validate_openai_key(api_key):
        click.echo("OpenAI API key is required. Set OPENAI_API_KEY env var or use --api-key", err=True)
        sys.exit(1)
    
    try:
        # Initialize components
        analyzer = CodebaseAnalyzer(
            root_path=Path(path),
            exclude_patterns=list(exclude),
            include_tests=include_tests
        )
        
        generator = DocumentationGenerator(
            api_key=api_key,
            model=model
        )
        
        # Analyze codebase
        click.echo("🔍 Analyzing codebase...")
        analysis = analyzer.analyze()
        
        if not analysis['files']:
            click.echo("No files found to analyze", err=True)
            sys.exit(1)
        
        click.echo(f"Found {len(analysis['files'])} files to document")
        
        # Generate documentation
        click.echo("Generating documentation with AI...")
        documentation = generator.generate_documentation(analysis)
        
        # Write to file
        output_path = Path(output)
        output_path.write_text(documentation, encoding='utf-8')
        
        click.echo(f"Documentation generated successfully: {output_path}")
        click.echo(f"Total tokens used: ~{generator.total_tokens}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    generate_docs()