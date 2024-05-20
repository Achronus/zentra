from cli.conf.storage import ComponentDetails


COMPONENT_DETAILS_DICT = {
    "Input": ComponentDetails(
        library="ui",
        filename="input.jsx",
        name="Input",
        child_names=[],
    ),
    "FileUpload": ComponentDetails(
        library="uploadthing",
        filename="file-upload.jsx",
        name="FileUpload",
        child_names=[],
    ),
    "Button": ComponentDetails(
        library="ui",
        filename="button.jsx",
        name="Button",
        child_names=[],
    ),
    "Calendar": ComponentDetails(
        library="ui",
        filename="calendar.jsx",
        name="Calendar",
        child_names=[],
    ),
    "Checkbox": ComponentDetails(
        library="ui",
        filename="checkbox.jsx",
        name="Checkbox",
        child_names=[],
    ),
    "Collapsible": ComponentDetails(
        library="ui",
        filename="collapsible.jsx",
        name="Collapsible",
        child_names=["CollapsibleTrigger", "CollapsibleContent"],
    ),
    "InputOTP": ComponentDetails(
        library="ui",
        filename="input-otp.jsx",
        name="InputOTP",
        child_names=["InputOTPGroup", "InputOTPSlot", "InputOTPSeparator"],
    ),
    "Label": ComponentDetails(
        library="ui",
        filename="label.jsx",
        name="Label",
        child_names=[],
    ),
    "RadioGroup": ComponentDetails(
        library="ui",
        filename="radio-group.jsx",
        name="RadioGroup",
        child_names=["RadioGroupItem"],
    ),
    "ScrollArea": ComponentDetails(
        library="ui",
        filename="scroll-area.jsx",
        name="ScrollArea",
        child_names=["ScrollBar"],
    ),
    "Separator": ComponentDetails(
        library="ui",
        filename="separator.jsx",
        name="Separator",
        child_names=[],
    ),
    "Select": ComponentDetails(
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
    ),
    "Slider": ComponentDetails(
        library="ui",
        filename="slider.jsx",
        name="Slider",
        child_names=[],
    ),
    "Textarea": ComponentDetails(
        library="ui",
        filename="textarea.jsx",
        name="Textarea",
        child_names=[],
    ),
    "Toggle": ComponentDetails(
        library="ui",
        filename="toggle.jsx",
        name="Toggle",
        child_names=[],
    ),
    "ToggleGroup": ComponentDetails(
        library="ui",
        filename="toggle-group.jsx",
        name="ToggleGroup",
        child_names=["ToggleGroupItem"],
    ),
    "Alert": ComponentDetails(
        library="ui",
        filename="alert.jsx",
        name="Alert",
        child_names=["AlertTitle", "AlertDescription"],
    ),
    "AlertDialog": ComponentDetails(
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
    ),
    "Tooltip": ComponentDetails(
        library="ui",
        filename="tooltip.jsx",
        name="Tooltip",
        child_names=["TooltipTrigger", "TooltipContent", "TooltipProvider"],
    ),
    "Avatar": ComponentDetails(
        library="ui",
        filename="avatar.jsx",
        name="Avatar",
        child_names=["AvatarImage", "AvatarFallback"],
    ),
    "Badge": ComponentDetails(
        library="ui",
        filename="badge.jsx",
        name="Badge",
        child_names=[],
    ),
    "Switch": ComponentDetails(
        library="ui",
        filename="switch.jsx",
        name="Switch",
        child_names=[],
    ),
    "Pagination": ComponentDetails(
        library="ui",
        filename="pagination.jsx",
        name="Pagination",
        child_names=[
            "PaginationContent",
            "PaginationEllipsis",
            "PaginationItem",
            "PaginationLink",
            "PaginationNext",
            "PaginationPrevious",
        ],
    ),
    "DropdownMenu": ComponentDetails(
        library="ui",
        filename="dropdown-menu.jsx",
        name="DropdownMenu",
        child_names=[
            "DropdownMenuTrigger",
            "DropdownMenuContent",
            "DropdownMenuItem",
            "DropdownMenuCheckboxItem",
            "DropdownMenuRadioItem",
            "DropdownMenuLabel",
            "DropdownMenuSeparator",
            "DropdownMenuShortcut",
            "DropdownMenuGroup",
            "DropdownMenuPortal",
            "DropdownMenuSub",
            "DropdownMenuSubContent",
            "DropdownMenuSubTrigger",
            "DropdownMenuRadioGroup",
        ],
    ),
    "Breadcrumb": ComponentDetails(
        library="ui",
        filename="breadcrumb.jsx",
        name="Breadcrumb",
        child_names=[
            "BreadcrumbList",
            "BreadcrumbItem",
            "BreadcrumbLink",
            "BreadcrumbPage",
            "BreadcrumbSeparator",
            "BreadcrumbEllipsis",
        ],
    ),
    "Accordion": ComponentDetails(
        library="ui",
        filename="accordion.jsx",
        name="Accordion",
        child_names=[
            "AccordionItem",
            "AccordionTrigger",
            "AccordionContent",
        ],
    ),
    "AspectRatio": ComponentDetails(
        library="ui",
        filename="aspect-ratio.jsx",
        name="AspectRatio",
        child_names=[],
    ),
    "Progress": ComponentDetails(
        library="ui",
        filename="progress.jsx",
        name="Progress",
        child_names=[],
    ),
}
