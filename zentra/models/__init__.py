from zentra.core import Component, Page, Zentra
from zentra.models.demo.agency_details import agency_details
from zentra.models.demo.user_button import user_btn

# Web pages that contain multiple React components
page_map: list[Page] = [
    agency_details,
]

# Single components that are not in pages
standalone_components: list[Component] = [
    user_btn,
]

# Setup the application
zentra = Zentra()

# Register the pages and components to generate
zentra.register(page_map)
zentra.register(standalone_components)
