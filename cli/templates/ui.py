class CalendarJSX:
    """A JSX storage container for the Zentra Calendar model."""

    @classmethod
    def unique_logic(cls) -> str:
        """Generates a string of JSX for the unique logic of the component."""
        return "const [date, setDate] = useState(new Date());"

    @classmethod
    def attributes(cls) -> str:
        """Generates a string of JSX containing the attributes of the component's root."""
        return 'mode="single" selected={date} onSelect={setDate} className="rounded-md border"'


class CheckboxJSX:
    """A JSX storage container for the Zentra Checkbox model."""

    @classmethod
    def main_content(cls, id: str, label: str) -> str:
        """Generates a string of JSX with the main content of the component."""
        return f'<div className="grid gap-1.5 leading-none"><label htmlFor="{id}" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">{label}</label>'

    @classmethod
    def more_info(cls, info: str) -> str:
        """Generates a string of JSX for the `more_info` optional argument."""
        return f'<p className="text-sm text-muted-foreground">{info}</p>'


class CollapsibleJSX:
    """A JSX storage container for the Zentra Collapsible model."""

    @classmethod
    def unique_logic(cls) -> str:
        """Generates a string of JSX for the unique logic of the component."""
        return "const [collapsibleIsOpen, setCollapsibleIsOpen] = useState(false);"

    @classmethod
    def attributes(cls) -> str:
        """Generates a string of JSX containing the attributes of the component's root."""
        return 'open={collapsibleIsOpen} onOpenChange={setCollapsibleIsOpen} className="w-[350px] space-y-2"'

    @classmethod
    def title(cls, title: str) -> str:
        """Generates a string of JSX for the title of the component."""
        return f'<div className="flex items-center justify-between space-x-4 px-4"><h4 className="text-sm font-semibold">{title}</h4><CollapsibleTrigger asChild><Button variant="ghost" size="sm" className="w-9 p-0"><ChevronsUpDown className="h-4 w-4" /><span className="sr-only">Toggle</span></Button></CollapsibleTrigger></div>'

    @classmethod
    def items(cls, items: list[str]) -> str:
        """Generates a string of JSX for the items of the component."""
        items_str = f'<div className="rounded-md border px-4 py-3 font-mono text-sm">{items[0]}</div><CollapsibleContent className="space-y-2">'

        if len(items) > 1:
            for item in items:
                items_str += f'<div className="rounded-md border px-4 py-3 font-mono text-sm">{item}</div>'

        items_str += "</CollapsibleContent>"
        return items_str
