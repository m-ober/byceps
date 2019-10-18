"""
byceps.events.snippet
~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from dataclasses import dataclass

from ..services.snippet.transfer.models import SnippetVersionID


@dataclass(frozen=True)
class _SnippetEvent:
    snippet_version_id: SnippetVersionID


@dataclass(frozen=True)
class SnippetCreated(_SnippetEvent):
    pass


@dataclass(frozen=True)
class SnippetUpdated(_SnippetEvent):
    pass