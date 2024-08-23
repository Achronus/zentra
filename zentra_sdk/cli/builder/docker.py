import os
import tarfile

import docker
from docker.models.containers import Container
from pydantic import BaseModel, PrivateAttr


class DockerBuilder(BaseModel):
    """Contains information and methods for using docker containers."""

    image_name: str
    container_name: str

    _client = PrivateAttr(None)

    def model_post_init(self, __context) -> None:
        self._client = docker.from_env()

    @property
    def client(self) -> docker.DockerClient:
        return self._client

    def use(self, path: str) -> None:
        """Performs a set of required docker operations: pull, run, copy, and cleanup."""
        self.pull()
        container = self.run()

        self.copy(container, path)
        self.cleanup(container)

    def pull(self) -> None:
        """Pulls the docker image."""
        self.client.images.pull(f"{self.image_name}:latest")

    def run(self) -> Container:
        """Runs the docker container."""
        return self.client.containers.run(
            f"{self.image_name}:latest",
            name=self.container_name,
            detach=True,
        )

    def copy(self, container: Container, path: str) -> None:
        bits, _ = container.get_archive(path=path)

        with open("temp.tar", "wb") as f:
            for chunk in bits:
                f.write(chunk)

        with tarfile.open("temp.tar") as tar:
            tar.extractall(path=".")

        os.remove("temp.tar")

    def cleanup(self, container: Container) -> None:
        """Stops a docker container and cleans up its files."""
        container.stop()
        container.remove()
        self.client.images.remove(self.image_name)
