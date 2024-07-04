"""
Interested in testing this file out?

Replace this file with `zentra/models/__init__.py`
"""

from zentra_models.core import File, Zentra

from zentra.models._demo.agency import agency_details


# Zentra File models that contain blocks of components
file_map: list[File] = [
    agency_details,  # Custom files here...
]

# Setup the application
zentra = Zentra()

# Register the files to generate
zentra.register(file_map)
