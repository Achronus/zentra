CALENDAR_VALID_VALS = {
    "attributes": 'mode="single" selected={testDate} onSelect={testSetDate} className="rounded-md border"',
    "unique_logic": "const [testDate, testSetDate] = useState(new Date());",
}

CHECKBOX_VALID_VALS = {
    "attributes": {
        "required": 'id="terms"',
        "with_disabled": 'id="terms" disabled',
    },
    "below_content": {
        "required": '<div className="grid gap-1.5 leading-none"><label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">Accept the terms and conditions.</label></div>',
        "with_optionals": '<div className="grid gap-1.5 leading-none"><label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">Accept the terms and conditions.</label><p className="text-sm text-muted-foreground">Pretty please!</p></div>',
    },
    "full_jsx": '<div className="flex items-top space-x-2"><Checkbox id="terms" disabled /><div className="grid gap-1.5 leading-none"><label htmlFor="terms" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">Accept the terms and conditions.</label><p className="text-sm text-muted-foreground">Pretty please!</p></div></div>',
}

COLLAPSIBLE_VALID_VALS = {
    "attributes": 'open={testIsOpen} onOpenChange={testSetIsOpen} className="w-[350px] space-y-2"',
    "unique_logic": "const [testIsOpen, testSetIsOpen] = useState(false);",
    "content": '<div className="flex items-center justify-between space-x-4 px-4"><h4 className="text-sm font-semibold">Starred repositories</h4><CollapsibleTrigger asChild><Button variant="ghost" size="sm" className="w-9 p-0"><ChevronsUpDown className="h-4 w-4" /><span className="sr-only">Toggle</span></Button></CollapsibleTrigger></div><div className="rounded-md border px-4 py-3 font-mono text-sm">Astrum-AI/Zentra</div><CollapsibleContent className="space-y-2"><div className="rounded-md border px-4 py-3 font-mono text-sm">Astrum-AI/Zentra</div><div className="rounded-md border px-4 py-3 font-mono text-sm">Not Zentra</div></CollapsibleContent>',
    "full_jsx": '<Collapsible open={testIsOpen} onOpenChange={testSetIsOpen} className="w-[350px] space-y-2"><div className="flex items-center justify-between space-x-4 px-4"><h4 className="text-sm font-semibold">Starred repositories</h4><CollapsibleTrigger asChild><Button variant="ghost" size="sm" className="w-9 p-0"><ChevronsUpDown className="h-4 w-4" /><span className="sr-only">Toggle</span></Button></CollapsibleTrigger></div><div className="rounded-md border px-4 py-3 font-mono text-sm">Astrum-AI/Zentra</div><CollapsibleContent className="space-y-2"><div className="rounded-md border px-4 py-3 font-mono text-sm">Astrum-AI/Zentra</div><div className="rounded-md border px-4 py-3 font-mono text-sm">Not Zentra</div></CollapsibleContent></Collapsible>',
}
