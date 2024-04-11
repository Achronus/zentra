CALENDAR_VALID_VALS = {
    "attributes": {
        "standard": 'mode="single" selected={monthlyDate} onSelect={monthlySetDate} className="rounded-md border"',
        "long_name": 'mode="single" selected={yearlyCalendarDate} onSelect={yearlyCalendarSetDate} className="rounded-md border"',
    },
    "logic": {
        "standard": "const [monthlyDate, monthlySetDate] = useState<Date | undefined>(new Date());",
        "long_name": "const [yearlyCalendarDate, yearlyCalendarSetDate] = useState<Date | undefined>(new Date());",
    },
    "imports": 'import { Calendar } from "@/components/ui/calendar"\nimport { useState } from "react"',
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
    "imports": 'import { Checkbox } from "@/components/ui/checkbox"',
    "content": {
        "standard": '<div className="flex items-top space-x-2">\n<Checkbox id="terms">\n<div className="grid gap-1.5 leading-none">\n<label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">\nAccept the terms and conditions.\n</label>\n</div>\n</Checkbox>\n</div>',
        "with_disabled": '<div className="flex items-top space-x-2">\n<Checkbox id="terms" disabled>\n<div className="grid gap-1.5 leading-none">\n<label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">\nAccept the terms and conditions.\n</label>\n<p className="text-sm text-muted-foreground">\nPretty please!\n</p>\n</div>\n</Checkbox>\n</div>',
    },
}

COLLAPSIBLE_VALID_VALS = {
    "attributes": 'open={testIsOpen} onOpenChange={testSetIsOpen} className="w-[350px] space-y-2"',
    "logic": "const [testIsOpen, testSetIsOpen] = useState(false);",
    "imports": 'import { Collapsible, CollapsibleTrigger, CollapsibleContent } from "@/components/ui/collapsible"\nimport { useState } from "react"\nimport { Button } from "@/components/ui/button"\nimport { ChevronsUpDown } from "lucide-react"',
    "content": '<Collapsible open={testIsOpen} onOpenChange={testSetIsOpen} className="w-[350px] space-y-2">\n<div className="flex items-center justify-between space-x-4 px-4">\n<h4 className="text-sm font-semibold">\nStarred repositories\n</h4>\n<CollapsibleTrigger asChild>\n<Button variant="ghost" size="sm" className="w-9 p-0">\n<ChevronsUpDown className="h-4 w-4" />\n<span className="sr-only">\nToggle\n</span>\n</Button>\n</CollapsibleTrigger>\n</div>\n<div className="rounded-md border px-4 py-3 font-mono text-sm">\nAstrum-AI/Zentra\n</div>\n<CollapsibleContent className="space-y-2">\n<div className="rounded-md border px-4 py-3 font-mono text-sm">\nNot Zentra\n</div>\n</CollapsibleContent>\n</Collapsible>',
}

INPUT_VALID_VALS = {
    "attributes": {
        "required": 'id="name" type="text" placeholder="Name"',
        "with_disabled": 'id="name" type="text" placeholder="Name" disabled',
    },
    "full_jsx": '<Input id="name" type="text" placeholder="Name" disabled />',
}

INPUTOTP_VALID_VALS = {
    "attributes": {
        "required": "maxLength={6}",
        "with_official_pattern": "maxLength={6} pattern={REGEXP_ONLY_DIGITS_AND_CHARS}",
        "with_custom_pattern": r'maxLength={6} pattern="([\^$.|?*+()\[\]{}])"',
    },
    "content": {
        "one_group": "<InputOTPGroup><InputOTPSlot index={0} /><InputOTPSlot index={1} /><InputOTPSlot index={2} /><InputOTPSlot index={3} /><InputOTPSlot index={4} /><InputOTPSlot index={5} /></InputOTPGroup>",
        "two_groups": "<InputOTPGroup><InputOTPSlot index={0} /><InputOTPSlot index={1} /><InputOTPSlot index={2} /></InputOTPGroup><InputOTPSeparator /><InputOTPGroup><InputOTPSlot index={3} /><InputOTPSlot index={4} /><InputOTPSlot index={5} /></InputOTPGroup>",
        "three_groups": "<InputOTPGroup><InputOTPSlot index={0} /><InputOTPSlot index={1} /></InputOTPGroup><InputOTPSeparator /><InputOTPGroup><InputOTPSlot index={2} /><InputOTPSlot index={3} /></InputOTPGroup><InputOTPSeparator /><InputOTPGroup><InputOTPSlot index={4} /><InputOTPSlot index={5} /></InputOTPGroup>",
    },
    "extra_imports": 'import { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp"',
    "full_jsx": "<InputOTP maxLength={6} pattern={REGEXP_ONLY_DIGITS_AND_CHARS}><InputOTPGroup><InputOTPSlot index={0} /><InputOTPSlot index={1} /><InputOTPSlot index={2} /></InputOTPGroup><InputOTPSeparator /><InputOTPGroup><InputOTPSlot index={3} /><InputOTPSlot index={4} /><InputOTPSlot index={5} /></InputOTPGroup></InputOTP>",
}

LABEL_VALID_VALS = {
    "attributes": 'htmlForm="terms"',
    "content": "Accept terms and conditions.",
    "full_jsx": '<Label htmlForm="terms">Accept terms and conditions.</Label>',
}
