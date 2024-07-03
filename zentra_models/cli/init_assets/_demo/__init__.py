"""
Interested in testing this file out?

Replace this file with `zentra/models/__init__.py`
"""

from zentra_models.core import Component, Page, Zentra

from zentra.models._demo.agency import agency_details
from zentra.models._demo.user_button import user_btn


# Web pages that contain multiple React components
page_map: list[Page] = [
    agency_details,  # Custom pages here...
]

# Single components that are not in pages
standalone_components: list[Component] = [
    user_btn,  # Custom components here...
]

# Setup the application
zentra = Zentra()

# Register the pages and components to generate
zentra.register(page_map)
zentra.register(standalone_components)
