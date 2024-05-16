# UI CONTROL COMPONENTS
CALENDAR_VALID_VALS = {
    "attributes": {
        "standard": 'mode="single" selected={monthlyDate} onSelect={monthlySetDate} className="rounded-md border"',
        "long_name": 'mode="single" selected={yearlyCalendarDate} onSelect={yearlyCalendarSetDate} className="rounded-md border"',
    },
    "logic": {
        "standard": "const [monthlyDate, monthlySetDate] = useState<Date | undefined>(new Date());",
        "long_name": "const [yearlyCalendarDate, yearlyCalendarSetDate] = useState<Date | undefined>(new Date());",
    },
    "content": {
        "standard": '<Calendar mode="single" selected={monthlyDate} onSelect={monthlySetDate} className="rounded-md border" />',
        "long_name": '<Calendar mode="single" selected={yearlyCalendarDate} onSelect={yearlyCalendarSetDate} className="rounded-md border" />',
    },
}

CHECKBOX_VALID_VALS = {
    "attributes": {
        "standard": 'id="terms" checked={false}',
        "with_disabled": 'id="terms" checked={false} disabled',
    },
    "content": {
        "standard": '<div className="flex items-top space-x-2">\n<Checkbox id="terms" checked={false}>\n<div className="grid gap-1.5 leading-none">\n<label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">\nAccept the terms and conditions.\n</label>\n</div>\n</Checkbox>\n</div>',
        "with_disabled": '<div className="flex items-top space-x-2">\n<Checkbox id="terms" checked={false} disabled>\n<div className="grid gap-1.5 leading-none">\n<label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">\nAccept the terms and conditions.\n</label>\n<p className="text-sm text-muted-foreground">\nPretty please!\n</p>\n</div>\n</Checkbox>\n</div>',
    },
}

COLLAPSIBLE_VALID_VALS = {
    "attributes": 'open={testIsOpen} onOpenChange={testSetIsOpen} className="w-[350px] space-y-2"',
    "logic": "const [testIsOpen, testSetIsOpen] = useState(false);",
    "content": '<Collapsible open={testIsOpen} onOpenChange={testSetIsOpen} className="w-[350px] space-y-2">\n<div className="flex items-center justify-between space-x-4 px-4">\n<h4 className="text-sm font-semibold">\nStarred repositories\n</h4>\n<CollapsibleTrigger asChild>\n<Button variant="ghost" size="sm" className="w-9 p-0">\n<ChevronsUpDown className="h-4 w-4" />\n<span className="sr-only">\nToggle\n</span>\n</Button>\n</CollapsibleTrigger>\n</div>\n<div className="rounded-md border px-4 py-3 font-mono text-sm">\nAstrum-AI/Zentra\n</div>\n<CollapsibleContent className="space-y-2">\n<div className="rounded-md border px-4 py-3 font-mono text-sm">\nNot Zentra\n</div>\n</CollapsibleContent>\n</Collapsible>',
}

INPUT_VALID_VALS = {
    "attributes": {
        "standard": 'id="name" type="text" placeholder="Name"',
        "with_disabled": 'id="name" type="text" placeholder="Name" disabled',
    },
    "content": {
        "standard": '<Input id="name" type="text" placeholder="Name" />',
        "with_disabled": '<Input id="name" type="text" placeholder="Name" disabled />',
    },
}

INPUTOTP_VALID_VALS = {
    "attributes": {
        "standard": "maxLength={6}",
        "pattern": "maxLength={6} pattern={REGEXP_ONLY_DIGITS_AND_CHARS}",
        "custom_pattern": r'maxLength={6} pattern="([\^$.|?*+()\[\]{}])"',
    },
    "content": {
        "one_group": "<InputOTP maxLength={6}>\n<InputOTPGroup>\n<InputOTPSlot index={0} />\n<InputOTPSlot index={1} />\n<InputOTPSlot index={2} />\n<InputOTPSlot index={3} />\n<InputOTPSlot index={4} />\n<InputOTPSlot index={5} />\n</InputOTPGroup>\n</InputOTP>",
        "two_groups": "<InputOTP maxLength={6} pattern={REGEXP_ONLY_DIGITS_AND_CHARS}>\n<InputOTPGroup>\n<InputOTPSlot index={0} />\n<InputOTPSlot index={1} />\n<InputOTPSlot index={2} />\n</InputOTPGroup>\n<InputOTPSeparator />\n<InputOTPGroup>\n<InputOTPSlot index={3} />\n<InputOTPSlot index={4} />\n<InputOTPSlot index={5} />\n</InputOTPGroup>\n</InputOTP>",
        "three_groups": '<InputOTP maxLength={6} pattern="([\^$.|?*+()\[\]{}])">\n<InputOTPGroup>\n<InputOTPSlot index={0} />\n<InputOTPSlot index={1} />\n</InputOTPGroup>\n<InputOTPSeparator />\n<InputOTPGroup>\n<InputOTPSlot index={2} />\n<InputOTPSlot index={3} />\n</InputOTPGroup>\n<InputOTPSeparator />\n<InputOTPGroup>\n<InputOTPSlot index={4} />\n<InputOTPSlot index={5} />\n</InputOTPGroup>\n</InputOTP>',
    },
}

LABEL_VALID_VALS = {
    "attributes": 'htmlFor="terms"',
    "content": '<Label htmlFor="terms">\nAccept terms and conditions.\n</Label>',
}

PAGINATION_VALID_VALS = {
    "content": {
        "simple": '<Pagination>\n<PaginationContent>\n<PaginationItem>\n<PaginationPrevious \nclassName={pagStartIndex === 0 ? "pointer-events-none opacity-50" : undefined}\n onClick={() => {\npagSetStartIndex(pagStartIndex - itemsPerPage);\npagSetEndIndex(pagEndIndex - itemsPerPage);\n}} />\n</PaginationItem>\n<PaginationItem>\n<PaginationLink href="#" isActive>1</PaginationLink>\n</PaginationItem>\n<PaginationItem>\n<PaginationLink href="#">2</PaginationLink>\n</PaginationItem>\n<PaginationItem>\n<PaginationLink href="#">3</PaginationLink>\n</PaginationItem>\n<PaginationItem>\n<PaginationNext \nclassName={pagEndIndex === maxitems ? "pointer-events-none opacity-50" : undefined}\n onClick={() => {\npagSetStartIndex(pagStartIndex + itemsPerPage);\npagSetEndIndex(pagEndIndex + itemsPerPage);\n}} />\n</PaginationItem>\n</PaginationContent>\n</Pagination>',
        "full": '<Pagination>\n<PaginationContent>\n<PaginationItem>\n<PaginationPrevious \nclassName={pagStartIndex === 0 ? "pointer-events-none opacity-50" : undefined}\n onClick={() => {\npagSetStartIndex(pagStartIndex - itemsPerPage);\npagSetEndIndex(pagEndIndex - itemsPerPage);\n}} />\n</PaginationItem>\n<PaginationItem>\n<PaginationLink href="#" isActive>1</PaginationLink>\n</PaginationItem>\n<PaginationItem>\n<PaginationLink href="#">2</PaginationLink>\n</PaginationItem>\n<PaginationItem>\n<PaginationLink href="#">3</PaginationLink>\n</PaginationItem>\n<PaginationItem>\n<PaginationEllipsis />\n</PaginationItem>\n<PaginationItem>\n<PaginationNext \nclassName={pagEndIndex === maxitems ? "pointer-events-none opacity-50" : undefined}\n onClick={() => {\npagSetStartIndex(pagStartIndex + itemsPerPage);\npagSetEndIndex(pagEndIndex + itemsPerPage);\n}} />\n</PaginationItem>\n</PaginationContent>\n</Pagination>',
    },
    "logic": {
        "simple": "const itemsPerPage = 10;\nconst maxItems = 100;\nconst [pagStartIndex, pagSetStartIndex] = useState(0);\nconst [pagEndIndex, pagSetEndIndex] = useState(itemsPerPage);",
        "full": "const itemsPerPage = 10;\nconst maxItems = 20;\nconst [pagStartIndex, pagSetStartIndex] = useState(0);\nconst [pagEndIndex, pagSetEndIndex] = useState(itemsPerPage);",
    },
}

RADIO_GROUP_VALID_VALS = {
    "attributes": 'defaultValue="comfortable"',
    "content": '<RadioGroup defaultValue="comfortable">\n<div className="flex items-center space-x-2">\n<RadioGroupItem value="default" id="r1" />\n<Label htmlFor="r1">\nDefault\n</Label>\n</div>\n<div className="flex items-center space-x-2">\n<RadioGroupItem value="comfortable" id="r2" />\n<Label htmlFor="r2">\nComfortable\n</Label>\n</div>\n<div className="flex items-center space-x-2">\n<RadioGroupItem value="compact" id="r3" />\n<Label htmlFor="r3">\nCompact\n</Label>\n</div>\n</RadioGroup>',
}

SCROLL_AREA_VALID_VALS = {
    "attributes": {
        "simple": 'className="w-96 rounded-md border"',
        "vertical": 'className="h-72 w-48 rounded-md border"',
        "horizontal": 'className="w-96 whitespace-nowrap rounded-md border"',
    },
    "content": {
        "simple": '<ScrollArea className="w-96 rounded-md border">\nThis is some text that is extremely simple.\n<ScrollBar orientation="vertical" />\n</ScrollArea>',
        "vertical": '<ScrollArea className="h-72 w-48 rounded-md border">\n<div className="p-4">\n<h4 className="mb-4 text-sm font-medium leading-none">\nTags\n</h4>\n{tags.map((tag) => (\n<>\n<div className="text-sm" key={tag}>\n{tag}\n</div>\n<Separator className="my-2" orientation="vertical" />\n</>\n))}\n</div>\n<ScrollBar orientation="vertical" />\n</ScrollArea>',
        "horizontal": '<ScrollArea className="w-96 whitespace-nowrap rounded-md border">\n<div className="flex w-max space-x-4 p-4">\n{works.map((artwork) => (\n<figure className="shrink-0" key={artwork.artist}>\n<div className="overflow-hidden rounded-md"\n<Image src={artwork.art} width={300} height={400} alt={`Photo by {artwork.artist}`} className="aspect-[3/4] h-fit w-fit object-cover" />\n</div>\n<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by\n<span className="font-semibold text-foreground">\n{artwork.artist}\n</span>\n</figcaption>\n</figure>\n))}\n</div>\n<ScrollBar orientation="horizontal" />\n</ScrollArea>',
    },
}

SELECT_VALID_VALS = {
    "content": {
        "single_group": '<Select>\n<SelectTrigger className="w-[280px]">\n<SelectValue placeholder="Select a fruit" />\n</SelectTrigger>\n<SelectGroup>\n<SelectLabel>Fruits</SelectLabel>\n<SelectItem value="apple">Apple</SelectItem>\n<SelectItem value="banana">Banana</SelectItem>\n</SelectGroup>\n</Select>',
        "single_group_no_label": '<Select>\n<SelectTrigger className="w-[280px]">\n<SelectValue placeholder="Select a fruit" />\n</SelectTrigger>\n<SelectItem value="apple">Apple</SelectItem>\n<SelectItem value="banana">Banana</SelectItem>\n</Select>',
        "multi_groups": '<Select>\n<SelectTrigger className="w-[280px]">\n<SelectValue placeholder="Select a fruit" />\n</SelectTrigger>\n<SelectGroup>\n<SelectLabel>Traditional</SelectLabel>\n<SelectItem value="apple">Apple</SelectItem>\n<SelectItem value="banana">Banana</SelectItem>\n</SelectGroup>\n<SelectGroup>\n<SelectLabel>Fancy</SelectLabel>\n<SelectItem value="blueberry">Blueberry</SelectItem>\n<SelectItem value="pineapple">Pineapple</SelectItem>\n</SelectGroup>\n</Select>',
    },
}

SLIDER_VALID_VALS = {
    "content": {
        "standard": '<Slider min={0} max={100} step={1} orientation="horizontal" defaultValue={[10]} className={cn("w-[60%]", className)} />',
        "all_params": '<Slider min={1} max={50} step={1} htmlFor="counts" disabled orientation="vertical" defaultValue={[10]} className={cn("w-[40%]", className)} />',
    },
}

SWITCH_VALID_VALS = {
    "content": {
        "standard": '<Switch id="airplaneMode" checked={false} />',
        "checked": '<Switch id="airplaneMode" checked={true} />',
        "disabled": '<Switch id="airplaneMode" checked={false} disabled />',
    }
}

TEXTAREA_VALID_VALS = {
    "content": '<Textarea id="message" placeholder="Type your message here." />'
}

TOGGLE_VALID_VALS = {
    "content": {
        "simple": '<Toggle pressed={false} aria-label="Toggle">\ntest {text}\n</Toggle>',
        "icon": '<Toggle pressed={false} aria-label="Toggle">\n<Italic className="mr-2 h-4 w-4" />\nicon {text}\n</Toggle>',
        "simple_full": '<Toggle size="sm" variant="outline" pressed={true} disabled aria-label="Toggle outline">\ntest {text}\n</Toggle>',
        "icon_full": '<Toggle size="lg" pressed={true} disabled aria-label="Toggle bold">\nicon {text}\n<Italic className="mr-2 h-4 w-4" />\n</Toggle>',
    },
}

TOGGLE_GROUP_VALID_VALS = {
    "content": {
        "simple": '<ToggleGroup type="multiple" orientation="horizontal">\n<ToggleGroupItem pressed={false} aria-label="Toggle">\n<Italic className="mr-2 h-4 w-4" />\n</ToggleGroupItem>\n<ToggleGroupItem pressed={false} aria-label="Toggle">\n<Bold className="mr-2 h-4 w-4" />\n</ToggleGroupItem>\n<ToggleGroupItem pressed={false} aria-label="Toggle">\n<Underline className="mr-2 h-4 w-4" />\n</ToggleGroupItem>\n</ToggleGroup>',
        "full": '<ToggleGroup type="single" disabled size="lg" variant="outline" orientation="vertical">\n<ToggleGroupItem pressed={true} aria-label="Toggle">\n<Italic className="mr-2 h-4 w-4" />\nitalic {text}\n</ToggleGroupItem>\n<ToggleGroupItem pressed={false} disabled aria-label="Toggle">\nbold {text}\n<Bold className="mr-2 h-4 w-4" />\n</ToggleGroupItem>\n<ToggleGroupItem pressed={false} aria-label="Toggle">\n<Underline className="mr-2 h-4 w-4" />\nundeline {text}\n</ToggleGroupItem>\n</ToggleGroup>',
    }
}

# UI NOTIFICATION COMPONENTS
ALERT_VALID_VALS = {
    "content": {
        "simple": "<Alert>\n<AlertTitle>\nHeads up!\n</AlertTitle>\n<AlertDescription>\nYou can add components to your app using the cli.\n</AlertDescription>\n</Alert>",
        "icon": '<Alert>\n<Terminal className="h-4 w-4" />\n<AlertTitle>\nHeads up!\n</AlertTitle>\n<AlertDescription>\nYou can add components to your app using the cli.\n</AlertDescription>\n</Alert>',
        "full": '<Alert variant="destructive">\n<AlertCircle className="h-4 w-4" />\n<AlertTitle>\nError\n</AlertTitle>\n<AlertDescription>\nYour session has expired. Please log in again.\n</AlertDescription>\n</Alert>',
    },
}

ALERT_DIALOG_VALID_VALS = {
    "content": {
        "simple": '<AlertDialog>\n<AlertDialogTrigger asChild>\n<Button variant="outline">\nDelete Account\n</Button>\n</AlertDialogTrigger>\n<AlertDialogContent>\n<AlertDialogHeader>\n<AlertDialogTitle>\nAre you absolutely sure?\n</AlertDialogTitle>\n<AlertDialogDescription>\nThis action cannot be undone. This will permanently delete your account and remove your data from our servers.\n</AlertDialogDescription>\n</AlertDialogHeader>\n<AlertDialogFooter>\n<AlertDialogCancel>\nCancel\n</AlertDialogCancel>\n<AlertDialogAction>\nContinue\n</AlertDialogAction>\n</AlertDialogFooter>\n</AlertDialogContent>\n</AlertDialog>',
    },
}

TOOLTIP_VALID_VALS = {
    "content": {
        "button": '<TooltipProvider>\n<Tooltip>\n<TooltipTrigger asChild>\n<Button variant="outline">\nHover\n</Button>\n</TooltipTrigger>\n<TooltipContent>\n<p>Add to Library</p>\n</TooltipContent>\n</Tooltip>\n</TooltipProvider>',
        "string": "<TooltipProvider>\n<Tooltip>\n<TooltipTrigger asChild>\nTest tooltip\n</TooltipTrigger>\n<TooltipContent>\n<p>A cheeky label</p>\n</TooltipContent>\n</Tooltip>\n</TooltipProvider>",
        "icon": '<TooltipProvider>\n<Tooltip>\n<TooltipTrigger asChild>\n<Loader className="mr-2 h-4 w-4" size={30} />\n</TooltipTrigger>\n<TooltipContent>\n<p>Loading...</p>\n</TooltipContent>\n</Tooltip>\n</TooltipProvider>',
        "icon_text": '<TooltipProvider>\n<Tooltip>\n<TooltipTrigger asChild>\n<Loader className="mr-2 h-4 w-4" />\nLoading\n</TooltipTrigger>\n<TooltipContent>\n<p>Load me up!</p>\n</TooltipContent>\n</Tooltip>\n</TooltipProvider>',
    },
}

# UI PRESENTATION COMPONENTS
SEPARATOR_VALID_VALS = {
    "content": {
        "simple": '<Separator orientation="vertical" />',
        "full": '<Separator className="mx-4" orientation="horizontal" />',
    }
}

AVATAR_VALID_VALS = {
    "content": {
        "url": '<Avatar>\n<AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />\n<AvatarFallback>CN</AvatarFallback>\n</Avatar>',
        "path": '<Avatar>\n<AvatarImage src="/profile.png" alt={`Awesome photo of {me}`} />\n<AvatarFallback>AA</AvatarFallback>\n</Avatar>',
        "static_img": "<Avatar>\n<AvatarImage src={profilePic} alt={`Awesome photo of {me}`} />\n<AvatarFallback>AA</AvatarFallback>\n</Avatar>",
    }
}

BADGE_VALID_VALS = {
    "content": {
        "simple": "<Badge>\nBadge\n</Badge>",
        "variant": '<Badge variant="outline">\nBadge\n</Badge>',
    }
}

ACCORDION_VALID_VALS = {
    "content": {
        "simple": '<Accordion type="single" className="w-full" collapsible>\n<AccordionItem value="item-1">\n<AccordionTrigger>\nIs it accessible?\n</AccordionTrigger>\n<AccordionContent>\nYes. It adheres to the WAI-ARIA design pattern.\n</AccordionContent>\n</AccordionItem>\n<AccordionItem value="item-2">\n<AccordionTrigger>\nIs it styled?\n</AccordionTrigger>\n<AccordionContent>\nYes. It comes with default styles that matches the other components\' aesthetic.\n</AccordionContent>\n</AccordionItem>\n<AccordionItem value="item-3">\n<AccordionTrigger>\nIs it animated?\n</AccordionTrigger>\n<AccordionContent>\nYes. It\'s animated by default, but you can disable it if you prefer.\n</AccordionContent>\n</AccordionItem>\n<AccordionItem value="item-4" disabled>\n<AccordionTrigger>\nCan I access it?\n</AccordionTrigger>\n<AccordionContent>\nNot today.\n</AccordionContent>\n</AccordionItem>\n</Accordion>',
        "full": '<Accordion type="multiple" disabled orientation="horizontal">\n<AccordionItem value="item-1">\n<AccordionTrigger>\nCan I access it?\n</AccordionTrigger>\n<AccordionContent>\nNot today.\n</AccordionContent>\n</AccordionItem>\n</Accordion>',
    },
}

# UI NAVIGATION COMPONENTS
DROPDOWN_MENU_VALID_VALS = {
    "content": {
        "radio_group": '<DropdownMenu>\n<DropdownMenuTrigger asChild>\n<Button variant="outline">\nopen\n</Button>\n</DropdownMenuTrigger>\n<DropdownMenuContent className="w-56">\n<DropdownMenuLabel>\nPanel Position\n</DropdownMenuLabel>\n<DropdownMenuSeparator />\n<DropdownMenuRadioGroup value={position} onValueChange={setPosition}>\n<DropdownMenuRadioItem value="top">\nTop Position\n</DropdownMenuRadioItem>\n<DropdownMenuRadioItem value="bottom">\nBottom Position\n</DropdownMenuRadioItem>\n<DropdownMenuRadioItem value="right">\nRight Position\n</DropdownMenuRadioItem>\n</DropdownMenuRadioGroup>\n</DropdownMenuContent>\n</DropdownMenu>',
        "checkbox": '<DropdownMenu>\n<DropdownMenuTrigger asChild>\n<Button variant="outline">\nopen\n</Button>\n</DropdownMenuTrigger>\n<DropdownMenuContent className="w-56">\n<DropdownMenuLabel>\nAppearance\n</DropdownMenuLabel>\n<DropdownMenuSeparator />\n<DropdownMenuCheckboxItem checked={ddCheckboxShowStatusBar} onCheckedChange={ddCheckboxSetShowStatusBar}>\nStatus Bar\n</DropdownMenuCheckboxItem>\n<DropdownMenuCheckboxItem checked={ddCheckboxShowActivityBar} onCheckedChange={ddCheckboxSetShowActivityBar}>\nActivity Bar\n</DropdownMenuCheckboxItem>\n<DropdownMenuCheckboxItem checked={ddCheckboxShowPanel} onCheckedChange={ddCheckboxSetShowPanel}>\nPanel\n</DropdownMenuCheckboxItem>\n</DropdownMenuContent>\n</DropdownMenu>',
        "str_list": '<DropdownMenu>\n<DropdownMenuTrigger>\nopen\n</DropdownMenuTrigger>\n<DropdownMenuContent className="w-56">\n<DropdownMenuLabel>\nPanel Position\n</DropdownMenuLabel>\n<DropdownMenuSeparator />\n<DropdownMenuGroup>\n<DropdownMenuItem>\nTop\n</DropdownMenuItem>\n<DropdownMenuItem>\nBottom\n</DropdownMenuItem>\n<DropdownMenuItem>\nRight\n</DropdownMenuItem>\n</DropdownMenuGroup>\n</DropdownMenuContent>\n</DropdownMenu>',
        "full": '<DropdownMenu>\n<DropdownMenuTrigger asChild>\n<Button variant="outline">\nopen\n</Button>\n</DropdownMenuTrigger>\n<DropdownMenuContent className="w-56">\n<DropdownMenuLabel>\nMy Account\n</DropdownMenuLabel>\n<DropdownMenuSeparator />\n<DropdownMenuGroup>\n<DropdownMenuItem>\n<User className="mr-2 h-4 w-4" />\n<span>Profile</span>\n<DropdownMenuShortcut>\n⇧⌘P\n</DropdownMenuShortcut>\n</DropdownMenuItem>\n<DropdownMenuItem>\n<CreditCard className="mr-2 h-4 w-4" />\n<span>Billing</span>\n<DropdownMenuShortcut>\n⌘B\n</DropdownMenuShortcut>\n</DropdownMenuItem>\n<DropdownMenuItem>\n<Settings className="mr-2 h-4 w-4" />\n<span>Settings</span>\n<DropdownMenuShortcut>\n⌘S\n</DropdownMenuShortcut>\n</DropdownMenuItem>\n<DropdownMenuItem>\n<Keyboard className="mr-2 h-4 w-4" />\n<span>Keyboard Shortcuts</span>\n<DropdownMenuShortcut>\n⌘K\n</DropdownMenuShortcut>\n</DropdownMenuItem>\n</DropdownMenuGroup>\n<DropdownMenuSeparator />\n<DropdownMenuGroup>\n<DropdownMenuItem>\n<Users className="mr-2 h-4 w-4" />\n<span>Team</span>\n</DropdownMenuItem>\n<DropdownMenuSub>\n<DropdownMenuSubTrigger>\n<UserPlus className="mr-2 h-4 w-4" />\n<span>Invite users</span>\n</DropdownMenuSubTrigger>\n<DropdownMenuPortal>\n<DropdownMenuSubContent>\n<DropdownMenuItem>\n<Mail className="mr-2 h-4 w-4" />\n<span>Email</span>\n</DropdownMenuItem>\n<DropdownMenuItem>\n<MessageSquare className="mr-2 h-4 w-4" />\n<span>Message</span>\n</DropdownMenuItem>\n<DropdownMenuSeparator />\n<DropdownMenuItem>\n<PlusCircle className="mr-2 h-4 w-4" />\n<span>More...</span>\n</DropdownMenuItem>\n</DropdownMenuSubContent>\n</DropdownMenuPortal>\n</DropdownMenuSub>\n<DropdownMenuItem>\n<Plus className="mr-2 h-4 w-4" />\n<span>New Team</span>\n<DropdownMenuShortcut>\n⌘+T\n</DropdownMenuShortcut>\n</DropdownMenuItem>\n</DropdownMenuGroup>\n<DropdownMenuSeparator />\n<DropdownMenuGroup>\n<DropdownMenuItem>\n<Github className="mr-2 h-4 w-4" />\n<span>Github</span>\n</DropdownMenuItem>\n<DropdownMenuItem>\n<LifeBuoy className="mr-2 h-4 w-4" />\n<span>Support</span>\n</DropdownMenuItem>\n<DropdownMenuItem disabled>\n<Cloud className="mr-2 h-4 w-4" />\n<span>API</span>\n</DropdownMenuItem>\n<DropdownMenuSeparator />\n<DropdownMenuItem>\n<LogOut className="mr-2 h-4 w-4" />\n<span>Log out</span>\n<DropdownMenuShortcut>\n⇧⌘Q\n</DropdownMenuShortcut>\n</DropdownMenuItem>\n</DropdownMenuGroup>\n</DropdownMenuContent>\n</DropdownMenu>',
        "no_label": '<DropdownMenu>\n<DropdownMenuTrigger>\nopen\n</DropdownMenuTrigger>\n<DropdownMenuContent className="w-56">\n<DropdownMenuGroup>\n<DropdownMenuItem>\nTop\n</DropdownMenuItem>\n<DropdownMenuItem>\nBottom\n</DropdownMenuItem>\n<DropdownMenuItem>\nRight\n</DropdownMenuItem>\n</DropdownMenuGroup>\n</DropdownMenuContent>\n</DropdownMenu>',
        "with_links": '<DropdownMenu>\n<DropdownMenuTrigger>\nopen\n</DropdownMenuTrigger>\n<DropdownMenuContent className="w-56">\n<DropdownMenuLabel>\nAccount Settings\n</DropdownMenuLabel>\n<DropdownMenuSeparator />\n<DropdownMenuGroup>\n<DropdownMenuLabel>\nCore Settings\n</DropdownMenuLabel>\n<DropdownMenuItem>\n<User className="mr-2 h-4 w-4" />\n<span>Profile</span>\n</DropdownMenuItem>\n<DropdownMenuItem disabled asChild>\n<Link href="/billing">\n<CreditCard className="mr-2 h-4 w-4" />\n<span>Billing</span>\n<DropdownMenuShortcut>\n⌘B\n</DropdownMenuShortcut>\n</Link>\n</DropdownMenuItem>\n<DropdownMenuItem asChild>\n<Link href="/settings">\n<span>Settings</span>\n</Link>\n</DropdownMenuItem>\n<DropdownMenuItem asChild>\n<Link href="/settings">\n<span>Settings</span>\n<DropdownMenuShortcut>\n⌘B\n</DropdownMenuShortcut>\n</Link>\n</DropdownMenuItem>\n</DropdownMenuGroup>\n</DropdownMenuContent>\n</DropdownMenu>',
    },
    "logic": {
        "radio_group": 'const [ddTopPosition, ddSetTopPosition] = useState("top")\nconst [ddBottomPosition, ddSetBottomPosition] = useState("bottom")\nconst [ddRightPosition, ddSetRightPosition] = useState("right")',
        "checkbox": "const [ddCheckboxShowStatusBar, ddCheckboxSetShowStatusBar] = useState<Checked>(true);\nconst [ddCheckboxShowActivityBar, ddCheckboxSetShowActivityBar] = useState<Checked>(false);\nconst [ddCheckboxShowPanel, ddCheckboxSetShowPanel] = useState<Checked>(false);",
        "str_list": "",
        "full": "",
    },
}

BREADCRUMB_VALID_VALS = {
    "content": {
        "ellipsis_trigger": '<Breadcrumb>\n<BreadcrumbList>\n<BreadcrumbItem>\n<BreadcrumbLink href="/">\nHome\n</BreadcrumbLink>\n</BreadcrumbItem>\n<BreadcrumbSeparator />\n<BreadcrumbItem>\n<DropdownMenu>\n<DropdownMenuTrigger className="flex items-center gap-1">\n<BreadcrumbEllipsis className="h-4 w-4" />\n<span className="sr-only">Toggle menu</span>\n</DropdownMenuTrigger>\n<DropdownMenuContent align="start">\n<DropdownMenuGroup>\n<DropdownMenuItem asChild>\n<Link href="/docs">\n<span>Documentation</span>\n</Link>\n</DropdownMenuItem>\n<DropdownMenuItem asChild>\n<Link href="/themes">\n<span>Themes</span>\n</Link>\n</DropdownMenuItem>\n<DropdownMenuItem asChild>\n<Link href="/github">\n<span>GitHub</span>\n</Link>\n</DropdownMenuItem>\n</DropdownMenuGroup>\n</DropdownMenuContent>\n</DropdownMenu>\n</BreadcrumbItem>\n<BreadcrumbSeparator />\n<BreadcrumbItem>\n<BreadcrumbLink href="/docs/components">\nComponents\n</BreadcrumbLink>\n</BreadcrumbItem>\n<BreadcrumbSeparator />\n<BreadcrumbItem>\n<BreadcrumbPage>\nBreadcrumb\n</BreadcrumbPage>\n</BreadcrumbItem>\n</BreadcrumbList>\n</Breadcrumb>',
        "text_trigger": '<Breadcrumb>\n<BreadcrumbList>\n<BreadcrumbItem>\n<BreadcrumbLink href="/">\nHome\n</BreadcrumbLink>\n</BreadcrumbItem>\n<BreadcrumbSeparator>\n<Slash />\n</BreadcrumbSeparator>\n<BreadcrumbItem>\n<DropdownMenu>\n<DropdownMenuTrigger className="flex items-center gap-1">\nComponents\n<ChevronDown className="h-4 w-4" />\n</DropdownMenuTrigger>\n<DropdownMenuContent align="start">\n<DropdownMenuGroup>\n<DropdownMenuItem asChild>\n<Link href="/docs">\n<span>Documentation</span>\n</Link>\n</DropdownMenuItem>\n<DropdownMenuItem asChild>\n<Link href="/themes">\n<span>Themes</span>\n</Link>\n</DropdownMenuItem>\n<DropdownMenuItem asChild>\n<Link href="/github">\n<span>GitHub</span>\n</Link>\n</DropdownMenuItem>\n</DropdownMenuGroup>\n</DropdownMenuContent>\n</DropdownMenu>\n</BreadcrumbItem>\n<BreadcrumbSeparator>\n<Slash />\n</BreadcrumbSeparator>\n<BreadcrumbItem>\n<BreadcrumbLink href="/docs/components">\nComponents\n</BreadcrumbLink>\n</BreadcrumbItem>\n<BreadcrumbSeparator>\n<Slash />\n</BreadcrumbSeparator>\n<BreadcrumbItem>\n<BreadcrumbPage>\nBreadcrumb\n</BreadcrumbPage>\n</BreadcrumbItem>\n</BreadcrumbList>\n</Breadcrumb>',
    }
}


# CORE UI MAPPING
VALID_VALS_MAP = {
    "calendar": CALENDAR_VALID_VALS,
    "checkbox": CHECKBOX_VALID_VALS,
    "collapsible": COLLAPSIBLE_VALID_VALS,
    "input": INPUT_VALID_VALS,
    "input_otp": INPUTOTP_VALID_VALS,
    "label": LABEL_VALID_VALS,
    "radio_group": RADIO_GROUP_VALID_VALS,
    "scroll_area": SCROLL_AREA_VALID_VALS,
    "select": SELECT_VALID_VALS,
    "slider": SLIDER_VALID_VALS,
    "switch": SWITCH_VALID_VALS,
    "textarea": TEXTAREA_VALID_VALS,
    "toggle": TOGGLE_VALID_VALS,
    "toggle_group": TOGGLE_GROUP_VALID_VALS,
    "alert": ALERT_VALID_VALS,
    "alert_dialog": ALERT_DIALOG_VALID_VALS,
    "separator": SEPARATOR_VALID_VALS,
    "tooltip": TOOLTIP_VALID_VALS,
    "avatar": AVATAR_VALID_VALS,
    "badge": BADGE_VALID_VALS,
    "pagination": PAGINATION_VALID_VALS,
    "dropdown_menu": DROPDOWN_MENU_VALID_VALS,
    "breadcrumb": BREADCRUMB_VALID_VALS,
    "accordion": ACCORDION_VALID_VALS,
}


# NEXTJS COMPONENTS
IMAGE_VALID_VALS = {
    "attributes": 'src={artwork.art} width={300} height={400} alt={`Photo by {artwork.artist}`} className="aspect-[3/4] h-fit w-fit object-cover"',
    "content": {
        "standard": '<Image src={artwork.art} width={300} height={400} alt={`Photo by {artwork.artist}`} className="aspect-[3/4] h-fit w-fit object-cover" />',
        "no_styles": "<Image src={artwork.art} width={300} height={400} alt={`Photo by {artwork.artist}`} />",
        "with_url": '<Image src="http://example.com" width={300} height={400} alt={`Photo by {artwork.artist}`} />',
        "basic_alt": '<Image src="http://example.com" width={300} height={400} alt="Photo by author" />',
        "basic_path": '<Image src="/profile.png" width={300} height={400} alt="Photo by author" />',
        "static_img_src": "<Image src={profilePic} width={300} height={400} alt={`Photo by {artwork.artist}`} />",
    },
}

LINK_VALID_VALS = {
    "attributes": {
        "styles": 'href="/dashboard" className="rounded-md border"',
        "target": 'href="/dashboard" target="_blank"',
        "replace": 'href="/dashboard" replace',
        "scroll": 'href="/dashboard" scroll={false}',
        "prefetch_false": 'href="/dashboard" prefetch={false}',
        "prefetch_true": 'href="/dashboard" prefetch={true}',
        "href_url": 'href={{ pathname: "/dashboard", query: { name: "test", }, }}',
        "href_url_multi_query": 'href={{ pathname: "/dashboard", query: { name: "test", second: "test2", }, }}',
    },
    "content": {
        "standard": '<Link href="/dashboard" />',
        "with_text": '<Link href="/dashboard">\nDashboard\n</Link>',
        "full": '<Link className="rounded-md border" target="_blank" href={{ pathname: "/dashboard", query: { name: "test", }, }} replace scroll={false} prefetch={false}>\nDashboard\n</Link>',
    },
}


# CORE NEXTJS MAPPING
NEXTJS_VALID_VALS_MAP = {
    "image": IMAGE_VALID_VALS,
    "link": LINK_VALID_VALS,
}


# REACT COMPONENTS
LUCIDE_ICON_VALID_VALS = {
    "content": {
        "simple": '<Italic className="mr-2 h-4 w-4" />',
        "text": '<Italic className="mr-2 h-4 w-4" />\ntest tag',
        "text_end": 'test tag\n<Italic className="mr-2 h-4 w-4" />',
        "text_param": '<Italic className="mr-2 h-4 w-4" />\ntest {tag}',
        "text_param_end": 'test {tag}\n<Italic className="mr-2 h-4 w-4" />',
        "full": 'test {tag}\n<Italic className="mr-2 h-4 w-4" size={24} color="red" strokeWidth={2} />',
        "full_no_text": '<Italic className="mr-2 h-4 w-4" size={24} color="red" strokeWidth={2} />',
    },
}
