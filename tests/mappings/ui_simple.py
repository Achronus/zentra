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
        "standard": 'id="terms"',
        "with_disabled": 'id="terms" disabled',
    },
    "content": {
        "standard": '<div className="flex items-top space-x-2">\n<Checkbox id="terms">\n<div className="grid gap-1.5 leading-none">\n<label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">\nAccept the terms and conditions.\n</label>\n</div>\n</Checkbox>\n</div>',
        "with_disabled": '<div className="flex items-top space-x-2">\n<Checkbox id="terms" disabled>\n<div className="grid gap-1.5 leading-none">\n<label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">\nAccept the terms and conditions.\n</label>\n<p className="text-sm text-muted-foreground">\nPretty please!\n</p>\n</div>\n</Checkbox>\n</div>',
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

RADIO_GROUP_VALID_VALS = {
    "attributes": 'defaultValue="comfortable"',
    "content": '<RadioGroup defaultValue="comfortable">\n<div className="flex items-center space-x-2">\n<RadioGroupItem value="default" id="r1" />\n<Label htmlFor="r1">\nDefault\n</Label>\n</div>\n<div className="flex items-center space-x-2">\n<RadioGroupItem value="comfortable" id="r2" />\n<Label htmlFor="r2">\nComfortable\n</Label>\n</div>\n<div className="flex items-center space-x-2">\n<RadioGroupItem value="compact" id="r3" />\n<Label htmlFor="r3">\nCompact\n</Label>\n</div>\n</RadioGroup>',
}

SCROLL_AREA_VALID_VALS = {
    "attributes": 'className="w-96 rounded-md border"',
    "content": {
        "simple": '<ScrollArea className="w-96 rounded-md border">\nThis is some text that is extremely simple.\n<ScrollBar orientation="vertical" />\n</ScrollArea>',
        "vertical": '<ScrollArea className="w-96 rounded-md border">\n<div className="p-4">\n<h4 className="mb-4 text-sm font-medium leading-none">Tags</h4>\n{tags.map((tag) => (\n<>\n<div key={tag} className="text-sm">\n{tag}\n</div>\n<Separator className="my-2" />\n</>\n))}\n<div>Content below map</div>\n</div>\n<ScrollBar orientation="vertical" />\n</ScrollArea>',
        "horizontal": '<ScrollArea className="w-96 rounded-md border">\n<div className="flex w-max space-x-4 p-4">\n{works.map((artwork) => (\n<figure key={artwork.artist} className="shrink-0">\n<div className="overflow-hidden rounded-md">\n<Image\nsrc={artwork.art}\nalt={`Photo by ${artwork.artist}`}\nclassName="aspect-[3/4] h-fit w-fit object-cover"\nwidth={300}\nheight={400}\n/>\n</div>\n<figcaption className="pt-2 text-xs text-muted-foreground">\nPhoto by{" "}\n<span className="font-semibold text-foreground">\n{artwork.artist}\n</span>\n</figcaption>\n</figure>\n))}\n</div>\n<ScrollBar orientation="horizontal" />\n</ScrollArea>',
    },
}


VALID_VALS_MAP = {
    "calendar": CALENDAR_VALID_VALS,
    "checkbox": CHECKBOX_VALID_VALS,
    "collapsible": COLLAPSIBLE_VALID_VALS,
    "input": INPUT_VALID_VALS,
    "input_otp": INPUTOTP_VALID_VALS,
    "label": LABEL_VALID_VALS,
    "radio_group": RADIO_GROUP_VALID_VALS,
    "scroll_area": SCROLL_AREA_VALID_VALS,
}
