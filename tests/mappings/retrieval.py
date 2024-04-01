import textwrap


COMPONENT_GITHUB_VALID = {
    "root_dirs": ["ui", "uploadthing"],
    "file_folder_list": {
        "ui": {
            "base": {
                "files": [
                    "accordion.tsx",
                    "alert-dialog.tsx",
                    "alert.tsx",
                    "aspect-ratio.tsx",
                    "avatar.tsx",
                    "badge.tsx",
                    "breadcrumb.tsx",
                    "button.tsx",
                    "calendar.tsx",
                    "card.tsx",
                    "carousel.tsx",
                    "checkbox.tsx",
                    "collapsible.tsx",
                    "command.tsx",
                    "context-menu.tsx",
                    "dialog.tsx",
                    "drawer.tsx",
                    "dropdown-menu.tsx",
                    "form.tsx",
                    "hover-card.tsx",
                    "input-otp.tsx",
                    "input.tsx",
                    "label.tsx",
                    "menubar.tsx",
                    "navigation-menu.tsx",
                    "pagination.tsx",
                    "popover.tsx",
                    "progress.tsx",
                    "radio-group.tsx",
                    "resizable.tsx",
                    "scroll-area.tsx",
                    "select.tsx",
                    "separator.tsx",
                    "sheet.tsx",
                    "skeleton.tsx",
                    "slider.tsx",
                    "sonner.tsx",
                    "switch.tsx",
                    "table.tsx",
                    "tabs.tsx",
                    "textarea.tsx",
                    "toast.tsx",
                    "toaster.tsx",
                    "toggle-group.tsx",
                    "toggle.tsx",
                    "tooltip.tsx",
                    "use-toast.ts",
                ]
            },
            "templates": {"files": ["form-field.tsx", "form.tsx"]},
        },
        "uploadthing": {
            "base": {"files": ["file-upload.tsx"]},
            "lib": {"files": ["core.ts", "route.ts", "uploadthing.ts"]},
        },
    },
    "ui_storage": {
        "base": [
            "accordion.tsx",
            "alert-dialog.tsx",
            "alert.tsx",
            "aspect-ratio.tsx",
            "avatar.tsx",
            "badge.tsx",
            "breadcrumb.tsx",
            "button.tsx",
            "calendar.tsx",
            "card.tsx",
            "carousel.tsx",
            "checkbox.tsx",
            "collapsible.tsx",
            "command.tsx",
            "context-menu.tsx",
            "dialog.tsx",
            "drawer.tsx",
            "dropdown-menu.tsx",
            "form.tsx",
            "hover-card.tsx",
            "input-otp.tsx",
            "input.tsx",
            "label.tsx",
            "menubar.tsx",
            "navigation-menu.tsx",
            "pagination.tsx",
            "popover.tsx",
            "progress.tsx",
            "radio-group.tsx",
            "resizable.tsx",
            "scroll-area.tsx",
            "select.tsx",
            "separator.tsx",
            "sheet.tsx",
            "skeleton.tsx",
            "slider.tsx",
            "sonner.tsx",
            "switch.tsx",
            "table.tsx",
            "tabs.tsx",
            "textarea.tsx",
            "toast.tsx",
            "toaster.tsx",
            "toggle-group.tsx",
            "toggle.tsx",
            "tooltip.tsx",
            "use-toast.ts",
        ],
        "templates": ["form-field.tsx", "form.tsx"],
        "lib": None,
    },
    "ut_storage": {
        "base": ["file-upload.tsx"],
        "templates": None,
        "lib": ["core.ts", "route.ts", "uploadthing.ts"],
    },
}

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
    "full_file": textwrap.dedent("""
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
    """),
}
