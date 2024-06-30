import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/zentra/ui/form'

type Props = {
  data?: string
}

const ZentraFormField = ({ data }: Props) => {
  return (
    <FormField
      disabled={isLoading}
      control={form.control}
      name=**FORM_FIELD_NAME**
      render={({ field }) => (
      <FormItem>
        <div>
          <FormLabel>**LABEL_TEXT**</FormLabel>
          <FormDescription>**DESC_TEXT**</FormDescription>
        </div>
        <FormControl>
          **FORM_CONTROL**
        </FormControl>
        <FormMessage />
      </FormItem>
      )}
    />
  )
};

export default ZentraFormField;
