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


def scroll_area_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="scroll-area.jsx",
        name="ScrollArea",
        child_names=["ScrollBar"],
    )


def separator_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="separator.jsx",
        name="Separator",
        child_names=[],
    )


def select_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="select.jsx",
        name="Select",
        child_names=[
            "SelectContent",
            "SelectGroup",
            "SelectItem",
            "SelectLabel",
            "SelectTrigger",
            "SelectValue",
        ],
    )


def slider_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="slider.jsx",
        name="Slider",
        child_names=[],
    )


def switch_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="switch.jsx",
        name="Switch",
        child_names=[],
    )


def textarea_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="textarea.jsx",
        name="Textarea",
        child_names=[],
    )


def toggle_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="toggle.jsx",
        name="Toggle",
        child_names=[],
    )


def toggle_group_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="toggle-group.jsx",
        name="ToggleGroup",
        child_names=["ToggleGroupItem"],
    )


def alert_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="alert.jsx",
        name="Alert",
        child_names=["AlertTitle", "AlertDescription"],
    )


def alert_dialog_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="alert-dialog.jsx",
        name="AlertDialog",
        child_names=[
            "AlertDialogPortal",
            "AlertDialogOverlay",
            "AlertDialogTrigger",
            "AlertDialogContent",
            "AlertDialogHeader",
            "AlertDialogFooter",
            "AlertDialogTitle",
            "AlertDialogDescription",
            "AlertDialogAction",
            "AlertDialogCancel",
        ],
    )


def tooltip_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="tooltip.jsx",
        name="Tooltip",
        child_names=["TooltipTrigger", "TooltipContent", "TooltipProvider"],
    )


def avatar_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="avatar.jsx",
        name="Avatar",
        child_names=["AvatarImage", "AvatarFallback"],
    )


def badge_details() -> ComponentDetails:
    return ComponentDetails(
        library="ui",
        filename="badge.jsx",
        name="Badge",
        child_names=[],
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
        scroll_area_details(),
        select_details(),
        slider_details(),
        switch_details(),
        textarea_details(),
        toggle_details(),
        toggle_group_details(),
        alert_details(),
        alert_dialog_details(),
        separator_details(),
        tooltip_details(),
        avatar_details(),
        badge_details(),
    ]
