"""
Codebase analyzer - extracts and analyzes code structure
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import pathspec
import logging

logger = logging.getLogger(__name__)

class CodebaseAnalyzer:
    """Analyzes codebase structure and extracts relevant information."""
    
    # Default patterns to exclude
    DEFAULT_EXCLUDE_PATTERNS = [
        'node_modules/**',
        '.git/**',
        '__pycache__/**',
        '*.pyc',
        '.env*',
        'venv/**',
        'env/**',
        '.venv/**',
        'dist/**',
        'build/**',
        '*.log',
        '.DS_Store',
        'coverage/**',
        '.coverage',
        '*.min.js',
        '*.min.css',
        'package-lock.json',
        'yarn.lock',
        '.idea/**',
        '.vscode/**',
        '*.sqlite*',
        '*.db',
        'migrations/**',
        'static/**',
        'media/**',
        'uploads/**',
    ]
    
    # File extensions to analyze
    SUPPORTED_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'jsx',
        '.tsx': 'tsx',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
        '.cs': 'csharp',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.r': 'r',
        '.sql': 'sql',
        '.sh': 'bash',
        '.yml': 'yaml',
        '.yaml': 'yaml',
        '.json': 'json',
        '.xml': 'xml',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.md': 'markdown',
        '.txt': 'text',
        '.dockerfile': 'dockerfile',
        '.makefile': 'makefile',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
    }
    
    def __init__(self, root_path: Path, exclude_patterns: List[str] = None, include_tests: bool = False):
        self.root_path = root_path.resolve()
        self.exclude_patterns = (exclude_patterns or []) + self.DEFAULT_EXCLUDE_PATTERNS
        self.include_tests = include_tests
        
        if not include_tests:
            self.exclude_patterns.extend([
                'test/**',
                'tests/**',
                '*_test.py',
                'test_*.py',
                '*.test.js',
                '*.test.ts',
                '*.spec.js',
                '*.spec.ts',
            ])
        
        self.spec = pathspec.PathSpec.from_lines('gitwildmatch', self.exclude_patterns)
        
    def analyze(self) -> Dict[str, Any]:
        """Analyze the codebase and return structured information."""
        logger.info(f"Analyzing codebase at: {self.root_path}")
        
        analysis = {
            'project_info': self._get_project_info(),
            'structure': self._get_directory_structure(),
            'files': self._analyze_files(),
            'dependencies': self._get_dependencies(),
            'readme': self._get_readme_content(),
            'config_files': self._get_config_files(),
        }
        
        return analysis
    
    def _get_project_info(self) -> Dict[str, Any]:
        """Extract basic project information."""
        info = {
            'name': self.root_path.name,
            'path': str(self.root_path),
            'total_files': 0,
            'total_lines': 0,
            'languages': {},
        }
        
        # Count files and lines
        for file_path in self._get_code_files():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = len(f.readlines())
                    info['total_lines'] += lines
                    info['total_files'] += 1
                    
                    # Count by language
                    ext = file_path.suffix.lower()
                    lang = self.SUPPORTED_EXTENSIONS.get(ext, 'unknown')
                    info['languages'][lang] = info['languages'].get(lang, 0) + 1
                    
            except Exception as e:
                logger.warning(f"Error reading {file_path}: {e}")
        
        return info
    
    def _get_directory_structure(self) -> Dict[str, Any]:
        """Get directory structure as a tree."""
        def build_tree(path: Path, max_depth: int = 3, current_depth: int = 0) -> Dict:
            if current_depth >= max_depth:
                return {}
            
            tree = {}
            try:
                for item in sorted(path.iterdir()):
                    if self.spec.match_file(str(item.relative_to(self.root_path))):
                        continue
                    
                    if item.is_dir():
                        tree[item.name + '/'] = build_tree(item, max_depth, current_depth + 1)
                    else:
                        tree[item.name] = 'file'
            except PermissionError:
                pass
            
            return tree
        
        return build_tree(self.root_path)
    
    def _analyze_files(self) -> List[Dict[str, Any]]:
        """Analyze individual files."""
        files = []
        
        for file_path in self._get_code_files():
            try:
                file_info = self._analyze_file(file_path)
                if file_info:
                    files.append(file_info)
            except Exception as e:
                logger.warning(f"Error analyzing {file_path}: {e}")
        
        return files
    
    def _analyze_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Skip very large files (>100KB)
            if len(content) > 100000:
                logger.info(f"Skipping large file: {file_path}")
                return None
            
            relative_path = file_path.relative_to(self.root_path)
            ext = file_path.suffix.lower()
            
            file_info = {
                'path': str(relative_path),
                'name': file_path.name,
                'extension': ext,
                'language': self.SUPPORTED_EXTENSIONS.get(ext, 'unknown'),
                'size': len(content),
                'lines': len(content.splitlines()),
                'content': content,
            }
            
            # Extract additional info based on file type
            if ext == '.py':
                file_info.update(self._analyze_python_file(content))
            elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                file_info.update(self._analyze_javascript_file(content))
            elif ext == '.md':
                file_info['type'] = 'documentation'
            elif ext in ['.yml', '.yaml', '.json', '.toml']:
                file_info['type'] = 'configuration'
            
            return file_info
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return None
    
    def _analyze_python_file(self, content: str) -> Dict[str, Any]:
        """Extract Python-specific information."""
        info = {'type': 'source'}
        
        # Simple regex-based extraction (could be improved with AST)
        import re
        
        # Find imports
        imports = re.findall(r'^(?:from\s+\S+\s+)?import\s+(.+)$', content, re.MULTILINE)
        info['imports'] = [imp.strip() for imp in imports if imp]
        
        # Find classes
        classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        info['classes'] = classes
        
        # Find functions
        functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
        info['functions'] = functions
        
        # Check if it's a test file
        if any(keyword in content.lower() for keyword in ['test', 'assert', 'unittest', 'pytest']):
            info['type'] = 'test'
        
        return info
    
    def _analyze_javascript_file(self, content: str) -> Dict[str, Any]:
        """Extract JavaScript/TypeScript-specific information."""
        info = {'type': 'source'}
        
        import re
        
        # Find imports/requires
        imports = re.findall(r'(?:import|require)\s*\([\'"]([^\'"]+)[\'"]\)', content)
        imports.extend(re.findall(r'import\s+.+\s+from\s+[\'"]([^\'"]+)[\'"]', content))
        info['imports'] = list(set(imports))
        
        # Find functions
        functions = re.findall(r'(?:function\s+(\w+)|(\w+)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))', content)
        info['functions'] = [f[0] or f[1] for f in functions if f[0] or f[1]]
        
        # Find classes
        classes = re.findall(r'class\s+(\w+)', content)
        info['classes'] = classes
        
        # Check if it's a test file
        if any(keyword in content.lower() for keyword in ['test', 'spec', 'describe', 'it(']):
            info['type'] = 'test'
        
        return info
    
    def _get_code_files(self) -> List[Path]:
        """Get all code files in the project."""
        files = []
        
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.root_path)
                
                # Check if file should be excluded
                if self.spec.match_file(str(relative_path)):
                    continue
                
                # Check if file extension is supported
                if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    files.append(file_path)
        
        return files
    
    def _get_dependencies(self) -> Dict[str, List[str]]:
        """Extract project dependencies."""
        deps = {}
        
        # Python dependencies
        for req_file in ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile']:
            req_path = self.root_path / req_file
            if req_path.exists():
                deps['python'] = self._parse_python_deps(req_path)
                break
        
        # JavaScript dependencies
        package_json = self.root_path / 'package.json'
        if package_json.exists():
            deps['javascript'] = self._parse_js_deps(package_json)
        
        return deps
    
    def _parse_python_deps(self, file_path: Path) -> List[str]:
        """Parse Python dependencies."""
        try:
            if file_path.name == 'requirements.txt':
                content = file_path.read_text()
                return [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
            elif file_path.name == 'package.json':
                import json
                data = json.loads(file_path.read_text())
                deps = []
                for dep_type in ['dependencies', 'devDependencies']:
                    if dep_type in data:
                        deps.extend(data[dep_type].keys())
                return deps
        except Exception as e:
            logger.warning(f"Error parsing dependencies from {file_path}: {e}")
        
        return []
    
    def _parse_js_deps(self, file_path: Path) -> List[str]:
        """Parse JavaScript dependencies."""
        try:
            import json
            data = json.loads(file_path.read_text())
            deps = []
            for dep_type in ['dependencies', 'devDependencies']:
                if dep_type in data:
                    deps.extend(data[dep_type].keys())
            return deps
        except Exception as e:
            logger.warning(f"Error parsing JS dependencies: {e}")
        
        return []
    
    def _get_readme_content(self) -> Optional[str]:
        """Get README content if available."""
        for readme_name in ['README.md', 'README.rst', 'README.txt', 'README']:
            readme_path = self.root_path / readme_name
            if readme_path.exists():
                try:
                    return readme_path.read_text(encoding='utf-8')
                except Exception as e:
                    logger.warning(f"Error reading README: {e}")
        
        return None
    
    def _get_config_files(self) -> List[Dict[str, str]]:
        """Get configuration files."""
        config_files = []
        config_patterns = [
            '*.yml', '*.yaml', '*.json', '*.toml', '*.ini', '*.cfg',
            'Dockerfile', 'docker-compose.yml', 'Makefile', '.env*'
        ]
        
        for pattern in config_patterns:
            for file_path in self.root_path.glob(pattern):
                if file_path.is_file():
                    try:
                        config_files.append({
                            'name': file_path.name,
                            'path': str(file_path.relative_to(self.root_path)),
                            'content': file_path.read_text(encoding='utf-8', errors='ignore')[:1000]  # First 1000 chars
                        })
                    except Exception as e:
                        logger.warning(f"Error reading config file {file_path}: {e}")
        
        return config_files