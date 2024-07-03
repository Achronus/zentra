from zentra_models.templates.storage import (
    JSXComponentContentStorage,
    JSXComponentExtras,
)
from zentra_models.templates.utils import dedupe


FORM_SCHEMA_BASE = """
const FormSchema = z.object({
  **form_schema**
});
"""

JSX_BASE = """**imports**

type Props = {
  **props**
}
**form_schema**
const PageName = (**prop_params**: Props) => {
  **logic**
  return (
      **content**
  );
};

export default PageName;
"""


def add_to_storage(
    local: JSXComponentExtras,
    comp_store: JSXComponentContentStorage | JSXComponentExtras,
    extend: bool = False,
) -> JSXComponentExtras:
    """A helper function for adding component items to storage. Returns the updated storage."""
    for key in local.__dict__.keys():
        if hasattr(comp_store, key):
            value = getattr(comp_store, key)
            if value:
                local_values: list[str] = getattr(local, key)
                local_values.extend(value) if extend else local_values.append(value)

    local.imports = dedupe(local.imports)
    local.logic = dedupe(local.logic)
    return local
