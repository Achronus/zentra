"use client"

import { useEffect } from 'react'
import { useForm } from 'react-hook-form'

import { zodResolver } from "@hookform/resolvers/zod"
import {z} from 'zod'

import { ZentraFormField } from '@/components/zentra/ui/form-field'

type CustomForm = {
  **FORM_FIELDS**
}

type Props = {
  data?: Partial<CustomForm>
}

// TODO: update schema if needed
// https://zod.dev/
const FormSchema = z.object({
  **SCHEMA_VALS_HERE**
});


const layout1 = ({ data }: Props) => {
  return (

  );
};

const layout2 = ({ data }: Props) => {
  return (

  );
};

const layout3 = ({ data }: Props) => {
  return (

  );
};

const ZentraForm = ({ data }: Props) => {
  const form = useForm<z.infer<typeof FormSchema>({
    mode: "onChange",
    resolver: zodResolver(FormSchema),
    defaultValues: {
      **FORM_DEFAULTS**
    }
  });

  const isLoading = form.formState.isSubmitting;

  useEffect(() => {
      if(data) {
          form.reset(data);
      }
  }, [data]);

  const handleSubmit = async (values: z.infer<typeof FormSchema>) => {
    try {
      console.log(values);
      // TODO: Update me
      // ...
    } catch (error) {
      console.log(error);
      // TODO: Update me
      // ...
    }
  };
  
  return (
  <Form {...form}>
    <form 
      onSubmit={form.handleSubmit(handleSubmit)}
      className='space-y-4'
    >
      **FORM_FIELDS_HERE**
    </form>
  </Form>
  )
};

export default ZentraForm;