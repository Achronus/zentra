"""
Interested in testing this file out?

Replace this file with `zentra/models/__init__.py`
"""

from zentra_models.core import Block, Page, Zentra

from zentra.models._demo.agency import agency_details
from zentra.models._demo.user_button import user_btn


# Web pages that contain multiple React components
page_map: list[Page] = [
    agency_details,  # Custom pages here...
]

# Single blocks that are not in pages
block_map: list[Block] = [
    user_btn,  # Custom blocks here...
]

# Setup the application
zentra = Zentra()

# Register the pages and blocks to generate
zentra.register(page_map)
zentra.register(block_map)
