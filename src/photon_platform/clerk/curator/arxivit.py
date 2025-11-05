"""
ArXiv reference utility - downloads papers and creates RST documentation
"""
from rich import print
import arxiv
from pathlib import Path
from slugify import slugify

def get_paper_data(paper_id: str) -> dict:
    """Fetch paper metadata from arXiv."""
    search = arxiv.Search(id_list=[paper_id])
    paper = next(search.results())
    
    return {
        'title': paper.title,
        'authors': [str(author) for author in paper.authors],
        'abstract': paper.summary,
        'published': paper.published,
        'categories': paper.categories,
        'comment': paper.comment,
        'doi': paper.doi,
        'journal_ref': paper.journal_ref,
        'primary_category': paper.primary_category,
        'paper_id': paper_id,
        'paper': paper
    }

def create_include_files(paper_dir: Path):
    """Create include files: premise, outline, quotes, and notes."""
    includes = {
        'premise.rst': """\
premise
~~~~~~~

""",
        'outline.rst': """\
outline
~~~~~~~

""",
        'quotes.rst': """\
quotes
~~~~~~

""",
        'notes.rst': """\
notes
~~~~~

""",
    }
    
    for filename, content in includes.items():
        include_path = paper_dir / filename
        include_path.write_text(content)
        print(f"Created include file: {include_path}")

def format_rst(data: dict) -> str:
    """Format paper data as RST document."""
    rst = f""".. _{slugify(data['title'])}:

{data['title']}
{'=' * len(data['title'])}

:id: {data['paper_id']}
:Authors: {', '.join(data['authors'])}
:Published: {data['published'].strftime('%Y-%m-%d')}
:arXiv: https://arxiv.org/abs/{data['paper_id']}
:PDF: https://arxiv.org/pdf/{data['paper_id']}
:DOI: {data['doi'] or 'N/A'}
:Journal Reference: {data['journal_ref'] or 'N/A'}
:Primary Category: {data['primary_category']}
:Categories: {', '.join(data['categories'])}
:Comment: {data['comment'] or 'N/A'}

:github_url: _

abstract
--------
{data['abstract']}

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst
"""
    return rst.strip()

def save_reference(paper_id: str, output_dir: str = '.') -> tuple[Path, Path]:
    """Save paper metadata as RST and download PDF."""
    data = get_paper_data(paper_id)
    rst_content = format_rst(data)

    # Create paper directory using slugified title
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    paper_dir = output_path / slugify(data['title'])
    paper_dir.mkdir(parents=True, exist_ok=True)
    
    # Create include files
    create_include_files(paper_dir)
    
    # Save index.rst
    index_path = paper_dir / 'index.rst'
    index_path.write_text(rst_content)
    print(f"Created RST file: {index_path}")
    
    # Download PDF
    pdf_path = data['paper'].download_pdf(str(paper_dir))
    print(f"Downloaded PDF: {pdf_path}")
    
    return index_path, pdf_path

def main():
    """Main entry point for command line usage."""
    import sys
    
    if len(sys.argv) == 2:
        paper_id = sys.argv[1]
    else:
        paper_id = input("Please enter the arXiv ID (e.g. 2208.04202): ").strip()
        
    if not paper_id:
        print("No arXiv ID provided")
        sys.exit(1)
        
    try:
        index_path, pdf_path = save_reference(paper_id)
        print("\n[green]✓ Successfully saved reference:[/green]")
        print(f"  RST: {index_path}")
        print(f"  PDF: {pdf_path}")
    except Exception as e:
        print(f"[red]Error processing arXiv ID:[/red] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
