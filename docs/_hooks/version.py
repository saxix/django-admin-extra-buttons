from __future__ import annotations

import posixpath
import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page
from re import Match

change_log = "/changelog.md"

def on_page_markdown(
    markdown: str, *, page: Page, config: MkDocsConfig, files: Files
):

    # Replace callback
    def replace(match: Match):
        type, args = match.groups()
        args = args.strip()
        if type in ["added", "add"]:
            return _badge_for_added(args, page, files)
        elif type in ["changed", "cgh"]:
            return _badge_for_change(args, page, files)

        # Otherwise, raise an error
        raise RuntimeError(f"Unknown shortcode: {type}")

    # Find and replace all external asset URLs in current page
    return re.sub(
        r"<!-- ver:(\w+)(.*?) -->",
        replace, markdown, flags = re.I | re.M
    )


def _badge(icon: str, text: str = "", type: str = ""):
    classes = f"mdx-badge mdx-badge--{type}" if type else "mdx-badge"
    return "".join([
        f"<span class=\"{classes}\">",
        *([f"<span class=\"mdx-badge__icon\">{icon}</span>"] if icon else []),
        *([f"<span class=\"mdx-badge__text\">{text}</span>"] if text else []),
        f"</span>",
    ])

def _badge_for_added(text: str, page: Page, files: Files):
    spec = text.replace(".", "")

    icon = "octicons-file-added-16"
    return _badge(
        icon = f"[:{icon}:]('Version added')",
        text = f" [{text}]({change_log}#{spec})" if spec else ""
    )

def _badge_for_change(text: str, page: Page, files: Files):
    spec = text.replace(".", "")
    icon = "material-square-edit-outline"
    return _badge(
        icon = f"[:{icon}:]('Version added')",
        text = f" [{text}]({change_log}#{spec})" if spec else ""
    )
