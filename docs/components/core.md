# zentra.core

The [`zentra.core`](#) module is the bread and butter of Zentra models. Here, you'll find the root containers and application entry point for all Zentra models. 

The ones you will often use are [`zentra.core.Page`](#zentracorepage) for creating React pages and [`zentra.core.Zentra`](#zentracorezentra) for initialising the application.

Others, such as [`zentra.core.Component`](#zentracorecomponent), are strictly used as base classes to inherit from [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel), enabling Pydantic functionality across all models. Typically, you won't use these, but they are useful to know about.

Here's a list of the [`zentra.core`](#) components:

<!-- no toc -->
- [zentra.core.Component](#zentracorecomponent)
- [zentra.core.Page](#zentracorepage)
- [zentra.core.Zentra](#zentracorezentra)

## zentra.core.Component

A base model for all Zentra model components. They are simple classes which inherit from [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel) to enable Pydantic functionality and standardise all component models.

### Attributes
```python
def function() -> None:
    pass
```

### Examples


## zentra.core.Page

## zentra.core.Zentra
