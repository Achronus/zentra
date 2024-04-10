VALID_IMPORTS = {
    "button": 'import { Button } from "@/components/ui/button"',
    "icon_button": {
        "standard": 'import { Button } from "@/components/ui/button"\nimport { Loader } from "lucide-react"',
        "with_url": 'import { Button } from "@/components/ui/button"\nimport { Loader } from "lucide-react"\nimport Link from "next/link"',
    },
    "calendar": 'import { Calendar } from "@/components/ui/calendar"',
    "checkbox": 'import { Checkbox } from "@/components/ui/checkbox"',
    "collapsible": [
        'import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible", import { Button } from "@/components/ui/button", import { ChevronsUpDown } from "lucide-react"'
    ],
    "input": 'import { Input } from "@/components/ui/input"',
    "input_otp": {
        "required": 'import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp"',
        "with_pattern": 'import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp"import { REGEXP_ONLY_DIGITS } from "input-otp"',
        "with_sep": 'import { InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot } from "@/components/ui/input-otp"',
        "all": [
            'import { InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot } from "@/components/ui/input-otp", import { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp"'
        ],
    },
    "label": 'import { Label } from "@/components/ui/label"\n',
}
