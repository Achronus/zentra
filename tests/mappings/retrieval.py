ZENTRA_INIT_VALID = {
    "config": "__init__.py",
    "demo_dir_path": "_demo",
    "demo_filenames": ["__init__.py", "agency_details.py", "user_button.py"],
}

ZENTRA_INIT_CODE_VALID = {
    "rawlines": [
        "from zentra.core import Component, Page, Zentra",
        "",
        "# Web pages that contain multiple React components",
        "page_map: list[Page] = [",
        "    # Custom pages here...",
        "]",
        "",
        "# Single components that are not in pages",
        "standalone_components: list[Component] = [",
        "    # Custom components here...",
        "]",
        "",
        "# Setup the application",
        "zentra = Zentra()",
        "",
        "# Register the pages and components to generate",
        "zentra.register(page_map)",
        "zentra.register(standalone_components)",
    ],
    "full_file": "from zentra.core import Component, Page, Zentra\n\n# Web pages that contain multiple React components\npage_map: list[Page] = [\n    # Custom pages here...\n]\n\n# Single components that are not in pages\nstandalone_components: list[Component] = [\n    # Custom components here...\n]\n\n# Setup the application\nzentra = Zentra()\n\n# Register the pages and components to generate\nzentra.register(page_map)\nzentra.register(standalone_components)",
}
