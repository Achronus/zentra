from cli.conf.storage import ComponentDetails


def input_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="input.jsx",
        name="Input",
        child_names=[],
    )


def file_upload_details() -> ComponentDetails:
    return ComponentDetails(
        library="uploadthing",
        filename="file-upload.jsx",
        name="FileUpload",
        child_names=[],
    )


def button_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="button.jsx",
        name="Button",
        child_names=[],
    )


def calendar_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="calendar.jsx",
        name="Calendar",
        child_names=[],
    )


def checkbox_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="checkbox.jsx",
        name="Checkbox",
        child_names=[],
    )


def collapsible_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="collapsible.jsx",
        name="Collapsible",
        child_names=["CollapsibleTrigger", "CollapsibleContent"],
    )


def input_otp_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="input-otp.jsx",
        name="InputOTP",
        child_names=["InputOTPGroup", "InputOTPSlot", "InputOTPSeparator"],
    )


def label_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="label.jsx",
        name="Label",
        child_names=[],
    )


def radio_group_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="radio-group.jsx",
        name="RadioGroup",
        child_names=["RadioGroupItem"],
    )


def component_details() -> list[ComponentDetails]:
    return [
        button_details(),
        calendar_details(),
        checkbox_details(),
        collapsible_details(),
        input_details(),
        input_otp_details(),
        label_details(),
        file_upload_details(),
        radio_group_details(),
    ]


COMPONENT_DETAILS_MAPPING = {
    "button": button_details(),
    "calendar": calendar_details(),
    "checkbox": checkbox_details(),
    "collapsible": collapsible_details(),
    "input": input_details(),
    "input_otp": input_otp_details(),
    "label": label_details(),
    "file_upload": file_upload_details(),
    "radio_group": radio_group_details(),
}
