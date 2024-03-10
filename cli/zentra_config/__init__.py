from zentra.core import Component, Page, Zentra

# Web pages that contain multiple React components
page_map: list[Page] = []

# Single components that are not in pages
standalone_components: list[Component] = []

# Setup the application
zentra = Zentra()

# Register the pages and components to generate
zentra.register(page_map)
zentra.register(standalone_components)
