from zentra.core import Component, Page, Zentra

# Web pages that contain multiple React components
page_map: list[Page] = [
    # Custom pages here...
]

# Single components that are not in pages
standalone_components: list[Component] = [
    # Custom components here...
]

# Setup the application
zentra = Zentra()

# Register the pages and components to generate
zentra.register(page_map)
zentra.register(standalone_components)
