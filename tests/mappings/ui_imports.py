VALID_IMPORTS = {
    "button": 'import { Button } from "../ui/button"\n',
    "icon_button": 'import { Button } from "../ui/button"\n',
    "calendar": '"use_client"\n\nimport { Calendar } from "../ui/calendar"\n',
    "checkbox": '"use_client"\n\nimport { Checkbox } from "../ui/checkbox"\n',
    "collapsible": '"use_client"\n\nimport { Collapsible, CollapsibleContent, CollapsibleTrigger } from "../ui/collapsible"\nimport { Button } from "../ui/button"\nimport { ChevronsUpDown } from "lucide-react"',
    "input": 'import { Input } from "../ui/input"\n',
    "input_otp": {
        "required": 'import { InputOTP, InputOTPGroup, InputOTPSlot } from "../ui/input-otp"\n',
        "with_pattern": 'import { InputOTP, InputOTPGroup, InputOTPSlot } from "../ui/input-otp"\nimport { REGEXP_ONLY_DIGITS } from "input-otp"',
        "with_sep": 'import { InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot } from "../ui/input-otp"\n',
        "all": 'import { InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot } from "../ui/input-otp"\nimport { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp"',
    },
    "label": 'import { Label } from "../ui/label"\n',
}
