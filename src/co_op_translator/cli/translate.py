"""
Translate command implementation for Co-op Translator CLI.
"""

import asyncio
import logging
import click
import importlib.resources
import yaml
import os
from pathlib import Path

from co_op_translator.core.project.project_translator import ProjectTranslator
from co_op_translator.config.base_config import Config
from co_op_translator.config.vision_config.config import VisionConfig

logger = logging.getLogger(__name__)


@click.command(name="translate")
@click.option(
    "--language-codes",
    "-l",
    required=True,
    help='Space-separated language codes for translation (e.g., "es fr de" or "all").',
)
@click.option(
    "--root-dir",
    "-r",
    default=".",
    help="Root directory of the project (default is current directory).",
)
@click.option(
    "--update",
    "-u",
    is_flag=True,
    help="Update translations by deleting and recreating them (Warning: Existing translations will be lost).",
)
@click.option("--images", "-img", is_flag=True, help="Only translate image files.")
@click.option("--markdown", "-md", is_flag=True, help="Only translate markdown files.")
@click.option("--notebook", "-n", is_flag=True, help="Only translate notebook files.")
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode.")
@click.option(
    "--fix",
    "-x",
    is_flag=True,
    help="Retranslate files with low confidence scores based on previous evaluation results.",
)
@click.option(
    "--min-confidence",
    "-c",
    default=0.7,
    type=float,
    help="Minimum confidence threshold (0.0-1.0) for identifying translations to fix. Only used with --fix.",
)
@click.option(
    "--fast",
    "-f",
    is_flag=True,
    help="Use fast mode for image translation (up to 3x faster at a slight cost to quality and alignment).",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Automatically confirm all prompts (useful for CI/CD pipelines).",
)
def translate_command(
    language_codes,
    root_dir,
    update,
    images,
    markdown,
    notebook,
    debug,
    fix,
    fast,
    yes,
    min_confidence,
):
    """
    CLI for translating project files.

    Usage examples:

    1. Default behavior (add new translations without deleting existing ones):
       translate -l "ko"
       translate -l "es fr de" -r "./my_project"

    2. Add only new Korean image translations (no existing translations are deleted):
       translate -l "ko" -img

    3. Add only new Korean notebook translations:
       translate -l "ko" -n

    4. Update all Korean translations (Warning: This deletes all existing Korean translations before re-translating):
       translate -l "ko" -u

    5. Update only Korean images (Warning: This deletes all existing Korean images before re-translating):
       translate -l "ko" -img -u

    6. Add new markdown translations for Korean without affecting other translations:
       translate -l "ko" -md

    7. Fix low confidence translations based on previous evaluation results:
       translate -l "ko" --fix

    8. Fix low confidence translations with custom threshold:
       translate -l "ko" --fix -c 0.8

    9. Fix low confidence translations for specific files only:
       translate -l "ko" --fix -md

    10. Use fast mode for image translation:
       translate -l "ko" -img -f

    Debug mode example:
    - translate -l "ko" -d: Enable debug logging.
    """

    try:
        # Check that the required environment variables are set
        Config.check_configuration()

        # Initialize translation mode
        cv_available = VisionConfig.check_configuration()

        # Determine translation mode based on flags and CV availability
        if not images and not markdown and not notebook:
            # Default: translate markdown and notebook files, images if CV available
            markdown = True
            notebook = True
            images = cv_available
        elif images and not cv_available:
            # User requested images but CV not available
            images = False
            click.echo(
                "Computer Vision is not configured: Image translation will be disabled."
            )
            click.echo(
                "To enable image translation, please add Computer Vision credentials to your environment variables."
            )
            click.echo("See the .env.template file for required variables.")

        # Log selected translation mode
        mode_msg = "🚀 Translation mode: "
        if images and markdown and notebook:
            mode_msg += "markdown, notebook and images"
        elif images and markdown:
            mode_msg += "markdown and images"
        elif images and notebook:
            mode_msg += "notebook and images"
        elif markdown and notebook:
            mode_msg += "markdown and notebook"
        elif markdown:
            mode_msg += "markdown only"
        elif notebook:
            mode_msg += "notebook only"
        elif images:
            mode_msg += "images only"
        else:
            mode_msg += "no files to translate"
        click.echo(mode_msg)

        if debug:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug("Debug mode enabled.")
        else:
            logging.basicConfig(level=logging.CRITICAL)

        # Validate root directory
        root_path = Path(root_dir).resolve()
        if not root_path.exists():
            raise click.ClickException(f"Root directory does not exist: {root_dir}")
        if not root_path.is_dir():
            raise click.ClickException(f"Root path is not a directory: {root_dir}")
        if not os.access(root_path, os.R_OK | os.W_OK):
            raise click.ClickException(
                f"Insufficient permissions for directory: {root_dir}"
            )

        # Show warning if 'all' is selected
        if language_codes == "all":
            click.echo(
                "Warning: Translating all languages at once can take a significant amount of time, especially when dealing with large markdown-based open-source projects that have many documents."
            )
            click.echo(
                "For better efficiency, it's recommended that contributors handle individual languages and upload their translations separately."
            )
            # Option to proceed or not
            if not yes:
                confirmation_all = click.prompt(
                    "Do you still want to proceed with translating all languages? Type 'yes' to continue",
                    type=str,
                )

                if confirmation_all.lower() != "yes":
                    click.echo("Translation for 'all' languages cancelled.")
                    return
                else:
                    click.echo("Proceeding with translation for all languages...")
            else:
                click.echo("Auto-confirming translation for all languages...")

            try:
                with importlib.resources.path(
                    "co_op_translator.fonts", "font_language_mappings.yml"
                ) as mappings_path:
                    with open(mappings_path, "r", encoding="utf-8") as file:
                        font_mappings = yaml.safe_load(file)
                        if not font_mappings:
                            raise click.ClickException("Empty font mappings file")
                        language_codes = " ".join(
                            [
                                lang_code
                                for lang_code in font_mappings
                                if isinstance(font_mappings[lang_code], dict)
                            ]
                        )
                        if not language_codes:
                            raise click.ClickException(
                                "No valid language codes found in font mappings"
                            )
                        logging.debug(
                            f"Loaded language codes from font mapping: {language_codes}"
                        )
            except (FileNotFoundError, yaml.YAMLError) as e:
                raise click.ClickException(f"Failed to load font mappings: {str(e)}")

        # Show warning and prompt if update is selected
        if update:
            click.echo(
                f"Warning: The update command will delete all existing translations for '{language_codes}' and re-translate everything."
            )
            if not yes:
                confirmation_update = click.prompt(
                    "Do you want to continue? Type 'yes' to proceed", type=str
                )

                if confirmation_update.lower() != "yes":
                    click.echo("Update cancelled by user.")
                    return
                else:
                    click.echo("Proceeding with update...")
            else:
                click.echo("Auto-confirming update operation...")

        # Initialize ProjectTranslator with determined settings
        translator = ProjectTranslator(
            language_codes, root_dir, markdown_only=markdown and not images
        )

        if fix:
            click.echo(f"Fixing translations with confidence below {min_confidence}...")

            # Fix is only applicable to markdown files, not images
            if images and not markdown:
                click.echo("Note: --fix only applies to markdown files, not images.")

            # Handle language codes
            if language_codes.lower() == "all":
                lang_list = Config.get_language_codes()
            else:
                lang_list = [code.strip() for code in language_codes.split()]

            total_retranslated = 0
            total_errors = 0

            for lang_code in lang_list:

                logger.info(f"Processing language: {lang_code}")

                try:
                    retranslated_count, errors = asyncio.run(
                        translator.retranslate_low_confidence_files(
                            lang_code, min_confidence
                        )
                    )

                    total_retranslated += retranslated_count
                    total_errors += len(errors)

                    if retranslated_count > 0:
                        logger.info(
                            f"{retranslated_count} files were retranslated successfully"
                        )
                    else:
                        logger.info(
                            f"No files with confidence below {min_confidence} were found or needed retranslation"
                        )

                    if errors:
                        logger.warning(
                            f"Errors during retranslation: {len(errors)} errors"
                        )
                        for error in errors:
                            logger.error(f"Error detail: {error}")
                except Exception as e:
                    logger.error(f"Error processing {lang_code}: {str(e)}")

            click.echo(f"\n{click.style('Summary:', fg='blue', bold=True)}")
            click.echo(
                f"Total files retranslated: {click.style(str(total_retranslated), fg='green')}"
            )
            if total_errors > 0:
                click.echo(f"Total errors: {click.style(str(total_errors), fg='red')}")

            logger.info(
                f"Project translation completed for languages: {language_codes}"
            )

        else:
            # Call translate_project with determined settings
            translator.translate_project(
                images=images,
                markdown=markdown,
                notebook=notebook,
                update=update,
                fast_mode=fast,
            )

            logger.info(
                f"Project translation completed for languages: {language_codes}"
            )

    except Exception as e:
        if debug:
            logger.exception("An error occurred during translation")
        raise click.ClickException(str(e))
