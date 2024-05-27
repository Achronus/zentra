VALID_IMPORTS = {
    # CONTROL COMPONENTS
    "button": {
        "simple": 'import { Button } from "@/components/ui/button"',
        "icon": 'import { Button } from "@/components/ui/button"\nimport { Loader } from "lucide-react"',
        "icon_url": [
            'import { Button } from "@/components/ui/button"',
            'import Link from "next/link"',
            'import { Loader } from "lucide-react"',
        ],
    },
    "calendar": {
        "single": '"use client"\nimport { useState } from "react"\nimport { Calendar } from "@/components/ui/calendar"',
        "multiple": '"use client"\nimport { useState } from "react"\nimport { Calendar } from "@/components/ui/calendar"',
        "range": '"use client"\nimport { useState } from "react"\nimport { Calendar } from "@/components/ui/calendar"\nimport { addDays } from "date-fns"\nimport { DateRange } from "react-day-picker"',
    },
    "checkbox": '"use client"\nimport { Checkbox } from "@/components/ui/checkbox"',
    "collapsible": '"use client"\nimport { useState } from "react"\nimport { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"\nimport { Button } from "@/components/ui/button"\nimport { ChevronsUpDown } from "lucide-react"',
    "input": 'import { Input } from "@/components/ui/input"',
    "input_otp": {
        "standard": 'import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp"',
        "pattern": 'import { InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot } from "@/components/ui/input-otp"\nimport { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp"',
        "custom_pattern": 'import { InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot } from "@/components/ui/input-otp"',
    },
    "label": 'import { Label } from "@/components/ui/label"',
    "pagination": '"use client"\nimport { useState } from "react"\nimport { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "@/components/ui/pagination"',
    "radio_group": 'import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"\nimport { Label } from "@/components/ui/label"',
    "scroll_area": {
        "simple": 'import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"',
        "vertical": 'import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"\nimport { Separator } from "@/components/ui/separator"',
        "horizontal": [
            'import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"',
            "import Image from 'next/image'",
        ],
    },
    "select": 'import { Select, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select"',
    "slider": 'import { Slider } from "@/components/ui/slider"\nimport { cn } from "@/lib/utils"',
    "switch": 'import { Switch } from "@/components/ui/switch"',
    "textarea": 'import { Textarea } from "@/components/ui/textarea"',
    "toggle": {
        "simple": 'import { Toggle } from "@/components/ui/toggle"',
        "icon": 'import { Toggle } from "@/components/ui/toggle"\nimport { Italic } from "lucide-react"',
    },
    "toggle_group": 'import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"\nimport { Bold, Italic, Underline } from "lucide-react"',
    "date_picker": {
        "single": '"use client"\nimport { useState } from "react"\nimport { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"\nimport { format } from "date-fns"\nimport { cn } from "@/lib/utils"\nimport { Calendar } from "@/components/ui/calendar"\nimport { Button } from "@/components/ui/button"\nimport { CalendarDays } from "lucide-react"',
        "multiple": '"use client"\nimport { useState } from "react"\nimport { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"\nimport { format } from "date-fns"\nimport { cn } from "@/lib/utils"\nimport { Calendar } from "@/components/ui/calendar"\nimport { Button } from "@/components/ui/button"\nimport { CalendarDays } from "lucide-react"',
        "range": '"use client"\nimport { useState } from "react"\nimport { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"\nimport { addDays, format } from "date-fns"\nimport { cn } from "@/lib/utils"\nimport { Calendar } from "@/components/ui/calendar"\nimport { DateRange } from "react-day-picker"\nimport { Button } from "@/components/ui/button"\nimport { CalendarDays } from "lucide-react"',
    },
    # NOTIFICATION COMPONENTS
    "alert": {
        "simple": 'import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"',
        "icon": 'import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"\nimport { Terminal } from "lucide-react"',
    },
    "alert_dialog": {
        "simple": 'import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog"'
    },
    "tooltip": {
        "button": 'import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"\nimport { Button } from "@/components/ui/button"',
        "string": 'import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"',
        "icon": 'import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"\nimport { Loader } from "lucide-react"',
    },
    # PRESENTATION COMPONENTS
    "separator": 'import { Separator } from "@/components/ui/separator"',
    "avatar": {
        "path_n_url": 'import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"',
        "static_img": [
            'import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"',
            "import profilePic from './me.png'",
        ],
    },
    "badge": 'import { Badge } from "@/components/ui/badge"',
    "accordion": 'import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"',
    "aspect_ratio": [
        'import { AspectRatio } from "@/components/ui/aspect-ratio"',
        "import Image from 'next/image'",
    ],
    "progress": {
        "simple": '"use client"\nimport { useState } from "react"\nimport { Progress } from "@/components/ui/progress"',
        "custom": '"use client"\nimport { useState } from "react"\nimport { Progress } from "@/components/ui/progress"',
    },
    "skeleton": 'import { Skeleton } from "@/components/ui/skeleton"',
    "table": {
        "text": 'import { Table, TableBody, TableCaption, TableCell, TableFooter, TableHead, TableHeader, TableRow } from "@/components/ui/table"',
        "map": 'import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from "@/components/ui/table"',
    },
    # NAVIGATION COMPONENTS
    "dropdown_menu": {
        "radio_group": '"use client"\nimport { useState } from "react"\nimport { DropdownMenu, DropdownMenuContent, DropdownMenuLabel, DropdownMenuRadioGroup, DropdownMenuRadioItem, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"\nimport { Button } from "@/components/ui/button"',
        "checkbox": '"use client"\nimport { useState } from "react"\nimport { DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"\nimport { Button } from "@/components/ui/button"',
        "str_list": 'import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"',
        "full": 'import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuLabel, DropdownMenuPortal, DropdownMenuSeparator, DropdownMenuShortcut, DropdownMenuSub, DropdownMenuSubContent, DropdownMenuSubTrigger, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"\nimport { Button } from "@/components/ui/button"\nimport { Cloud, CreditCard, Github, Keyboard, LifeBuoy, LogOut, Mail, MessageSquare, Plus, PlusCircle, Settings, User, UserPlus, Users } from "lucide-react"',
        "with_links": [
            'import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuShortcut, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"',
            "import Link from 'next/link'",
            'import { CreditCard, User } from "lucide-react"',
        ],
    },
    "breadcrumb": {
        "ellipsis_trigger": [
            'import { Breadcrumb, BreadcrumbEllipsis, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb"',
            "import Link from 'next/link'",
            'import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"',
        ],
        "text_trigger": [
            'import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb"',
            "import Link from 'next/link'",
            'import { ChevronDown, Slash } from "lucide-react"',
            'import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"',
        ],
    },
    "command": {
        "simple": 'import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"',
        "simple_links": 'import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"\nimport Link from \'next/link\'\nimport { Calendar, Smile } from "lucide-react"',
        "group_simple": 'import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"',
        "multi_groups": 'import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator, CommandShortcut } from "@/components/ui/command"\nimport { Calculator, Calendar, CreditCard, Settings, Smile, User } from "lucide-react"',
    },
    # MODAL COMPONENTS
    "popover": {
        "advanced": 'import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"\nimport { Button } from "@/components/ui/button"\nimport { Input } from "@/components/ui/input"\nimport { Label } from "@/components/ui/label"',
    },
}


NEXTJS_VALID_IMPORTS = {
    "image": {
        "standard": "import Image from 'next/image'",
        "static_src": "import Image from 'next/image'\nimport profilePic from './me.png'",
    },
    "link": "import Link from 'next/link'",
}

REACT_VALID_IMPORTS = {
    "lucide_icon": {
        "italic": 'import { Italic } from "lucide-react"',
        "loader": 'import { Loader } from "lucide-react"',
    }
}
