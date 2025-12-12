import click
from .logger import create_log_entry

@click.command()
@click.option('--title', prompt='Title', help='Title for log entry')
@click.option('--excerpt', prompt='Excerpt', help='Short description')
@click.option('--tags', prompt='Tags', help='Comma separated list of tags')
@click.option('--category', prompt='Category', help='Comma separated list of categories')
@click.option('--image', prompt='Image', default='', help='Path to image')
@click.pass_context
def log(ctx, title, excerpt, tags, category, image):
    """Creates a new log entry."""
    context = ctx.obj.get('context')
    
    if not context or not context.is_project:
        click.echo("Logger must be run within a project context.")
        return

    filename = create_log_entry(context.project_root, title, excerpt, tags, category, image)
    click.echo(f"Log entry created at: {filename}")
