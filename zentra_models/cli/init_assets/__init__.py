from zentra_models.core import ReactFile, Zentra

# Zentra File models that contain blocks of components
file_map: list[ReactFile] = [
    # Custom files here...
]

# Setup the application
zentra = Zentra()

# Register the files to generate
zentra.register(file_map)
