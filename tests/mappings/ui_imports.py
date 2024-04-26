VALID_IMPORTS = {
    "button": 'import { Button } from "@/components/ui/button"',
    "icon_button": {
        "standard": 'import { Button } from "@/components/ui/button"\nimport { Loader } from "lucide-react"',
        "with_url": 'import { Button } from "@/components/ui/button"\nimport Link from "next/link"\nimport { Loader } from "lucide-react"',
    },
    "calendar": 'import { Calendar } from "@/components/ui/calendar"\nimport { useState } from "react"',
    "checkbox": 'import { Checkbox } from "@/components/ui/checkbox"',
    "collapsible": 'import { Collapsible, CollapsibleTrigger, CollapsibleContent } from "@/components/ui/collapsible"\nimport { useState } from "react"\nimport { Button } from "@/components/ui/button"\nimport { ChevronsUpDown } from "lucide-react"',
    "input": 'import { Input } from "@/components/ui/input"',
    "input_otp": {
        "standard": 'import { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator } from "@/components/ui/input-otp"',
        "pattern": 'import { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator } from "@/components/ui/input-otp"\nimport { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp"',
        "custom_pattern": 'import { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator } from "@/components/ui/input-otp"',
    },
    "label": 'import { Label } from "@/components/ui/label"',
    "radio_group": 'import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"\nimport { Label } from "@/components/ui/label"',
    "scroll_area": {
        "simple": 'import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"',
        "vertical": 'import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"\nimport { Separator } from "@/components/ui/separator"',
        "horizontal": '''import Image from 'next/image'\nimport { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"''',
    },
    "select": 'import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select"',
}


NEXTJS_VALID_IMPORTS = {
    "image": {
        "standard": "import Image from 'next/image'",
        "static_src": "import Image from 'next/image'\nimport profilePic from './me.png'",
    },
    "link": "import Link from 'next/link'",
}
