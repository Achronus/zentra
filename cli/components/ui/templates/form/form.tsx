"use client"

// IMPORTS START
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import {z} from 'zod'

import { Form, **FORM_IMPORTS** } from '@/components/zentra/ui/form'

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

const **FORM_NAME** = ({ data }: Props) => {
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

export default **FORM_NAME**;