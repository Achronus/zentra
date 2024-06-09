from zentra.base.library import ShadcnUi
from zentra.core import Component


class InputOTPSlot(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui InputOTP](https://ui.shadcn.com/docs/components/input-otp) component. Represents a single `InputOTPSlot`.

    Cannot be used on its own. Must be used inside a `zentra.ui.control.InputOTP` model.

    Parameters:
    - `index` (`integer`) - the index position of the slot.
    """

    index: int
