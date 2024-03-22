---
hide:
  - navigation
---

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<a href="/" style="display: flex; justify-items: center;">![Zentra Logo](assets/imgs/zentra-logo.jpg)</a>

<p id="slogan" align="center">
    <em>Pydantic models to React components, fast, familiar, and easy to use</em>
</p>

---
<p id="version" align="center">
{{ version }}
</p>

<p id="badges" align="center">
    <a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
        <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
    </a>
    <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
        <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
    </a>
    <a href="https://pypi.org/project/fastapi" target="_blank">
        <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pypi.org/project/fastapi" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
    </a>
</p>

<div id="quick-links" style="display: flex; justify-content: center; align-items: center; gap: 3rem">
    <a href="/" target="_blank" style="text-align: center;">
        <svg xmlns="http://www.w3.org/2000/svg" height="32" width="28" viewBox="0 0 448 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(255, 255, 255, 0.7)" d="M96 0C43 0 0 43 0 96V416c0 53 43 96 96 96H384h32c17.7 0 32-14.3 32-32s-14.3-32-32-32V384c17.7 0 32-14.3 32-32V32c0-17.7-14.3-32-32-32H384 96zm0 384H352v64H96c-17.7 0-32-14.3-32-32s14.3-32 32-32zm32-240c0-8.8 7.2-16 16-16H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16zm16 48H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16s7.2-16 16-16z"/></svg>
        <p style="color: #fff; margin-top: 5px; margin-bottom: 5px;">Docs</p>
    </a>
    <a href="https://github.com/Astrum-AI/Zentra/" target="_blank"  style="text-align: center;">
        <svg xmlns="http://www.w3.org/2000/svg" height="32" width="28" viewBox="0 0 640 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(255, 255, 255, 0.7)" d="M392.8 1.2c-17-4.9-34.7 5-39.6 22l-128 448c-4.9 17 5 34.7 22 39.6s34.7-5 39.6-22l128-448c4.9-17-5-34.7-22-39.6zm80.6 120.1c-12.5 12.5-12.5 32.8 0 45.3L562.7 256l-89.4 89.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l112-112c12.5-12.5 12.5-32.8 0-45.3l-112-112c-12.5-12.5-32.8-12.5-45.3 0zm-306.7 0c-12.5-12.5-32.8-12.5-45.3 0l-112 112c-12.5 12.5-12.5 32.8 0 45.3l112 112c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L77.3 256l89.4-89.4c12.5-12.5 12.5-32.8 0-45.3z"/></svg>
        <p style="color: #fff; margin-top: 5px; margin-bottom: 5px;">Code</p>
    </a>
</div>

---

Zentra is a modern tool that uses [Pydantic](https://docs.pydantic.dev/latest/) models to create React components, fast. 


For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
