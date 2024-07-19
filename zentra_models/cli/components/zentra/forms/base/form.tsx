"use client";

import DynamicFormField from "@/components/DynamicFormField";
import ErrorPanel from "@/components/ErrorPanel";
import FileUploader from "@/components/FileUploader";
import { Loading } from "@/components/Loading";
import SubmitButton from "@/components/SubmitButton";
import { Form, FormControl } from "@/components/ui/form";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { SelectItem } from "@/components/ui/select";

import { FormFieldType, Gender, IdentificationTypes } from "@/types/enums";

import Image from "next/image";

const RegisterForm = () => {
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className={styles.container}>
        <section className="space-y-4">
          <h1 className="header">Getting Setup</h1>
          <p className="text-dark-700">Let us know more about you!</p>
        </section>

        <section className="space-y-4">
          <div className="mb-9 space-y-1">
            <h2 className="sub-header">Personal Information</h2>
          </div>
          <DynamicFormField
            fieldType={FormFieldType.INPUT}
            control={form.control}
            name="name"
            label="Full Name"
            placeholder="ex: Adam"
          />

          <div className="flex flex-col gap-6 xl:flex-row">
            <DynamicFormField
              fieldType={FormFieldType.INPUT}
              control={form.control}
              name="email"
              label="Email Address"
              placeholder="ex: johndoe@youremail.com"
              iconSrc="/icons/email.svg"
              iconAlt="email"
            />

            <DynamicFormField
              fieldType={FormFieldType.PHONE_INPUT}
              control={form.control}
              name="phone"
              label="Phone Number"
              placeholder="(555) 123-4567"
            />
          </div>

          <div className="flex flex-col gap-6 xl:flex-row">
            <DynamicFormField
              fieldType={FormFieldType.DATE_PICKER}
              control={form.control}
              name="birthDate"
              label="Date of Birth"
              placeholder="Select your birth date"
            />

            <DynamicFormField
              fieldType={FormFieldType.CUSTOM}
              control={form.control}
              name="gender"
              label="Gender"
              renderCustom={(field) => (
                <FormControl>
                  <RadioGroup
                    className="flex h-11 gap-6 xl:justify-between"
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    {Object.values(Gender).map((option) => (
                      <div key={option} className="radio-group">
                        <RadioGroupItem value={option} id={option} />
                        <Label htmlFor={option} className="cursor-pointer">
                          {option}
                        </Label>
                      </div>
                    ))}
                  </RadioGroup>
                </FormControl>
              )}
            />
          </div>

          <div className="flex flex-col gap-6 xl:flex-row">
            <DynamicFormField
              fieldType={FormFieldType.INPUT}
              control={form.control}
              name="address"
              label="Address"
              placeholder="ex: 14 New Road, Cambridge, UK"
            />

            <DynamicFormField
              fieldType={FormFieldType.INPUT}
              control={form.control}
              name="occupation"
              label="Occupation"
              placeholder="Software Engineer"
            />
          </div>

          <div className="flex flex-col gap-6 xl:flex-row">
            <DynamicFormField
              fieldType={FormFieldType.INPUT}
              control={form.control}
              name="emergencyContactName"
              label="Emergency Contact Name"
              placeholder="Guardian's name"
            />

            <DynamicFormField
              fieldType={FormFieldType.PHONE_INPUT}
              control={form.control}
              name="emergencyContactNumber"
              label="Emergency Contact Number"
              placeholder="ex: +447896458312"
            />
          </div>
        </section>

        <section className="space-y-4">
          <div className="mb-9 space-y-1">
            <h2 className="sub-header">Medical Information</h2>
          </div>
          <DynamicFormField
            fieldType={FormFieldType.SELECT}
            control={form.control}
            name="primaryPhysician"
            label="Primary Physician"
            placeholder="Select a physician"
          >
            {doctorsLoading && !doctors ? (
              <SelectItem value="loading">
                <Loading width={10} height={10} />
              </SelectItem>
            ) : (
              doctors &&
              doctors.map((doctor: Doctor) => (
                <SelectItem key={doctor.name} value={doctor.name}>
                  <div className="flex cursor-pointer items-center gap-2">
                    <Image
                      src={doctor.avatarIcon}
                      width={32}
                      height={32}
                      alt={doctor.name}
                      className="rounded-full border border-dark-500"
                    />
                    <p>{doctor.name}</p>
                  </div>
                </SelectItem>
              ))
            )}
          </DynamicFormField>

          <div className="flex flex-col gap-6 xl:flex-row">
            <DynamicFormField
              fieldType={FormFieldType.INPUT}
              control={form.control}
              name="insuranceProvider"
              label="Insurance Provider"
              placeholder="ex: Axa"
            />
            <DynamicFormField
              fieldType={FormFieldType.INPUT}
              control={form.control}
              name="insurancePolicyNumber"
              label="Insurance Policy Number"
              placeholder="ex: ABC123456789"
            />
          </div>

          <div className="flex flex-col gap-6 xl:flex-row">
            <DynamicFormField
              fieldType={FormFieldType.TEXTAREA}
              control={form.control}
              name="allergies"
              label="Allergies (if any)"
              placeholder="ex: Peanuts, Penicillin, Pollen"
            />
            <DynamicFormField
              fieldType={FormFieldType.TEXTAREA}
              control={form.control}
              name="currentMedication"
              label="Current Medications"
              placeholder="ex: Ibuprofen 200mg, Levothyroxine 50mcg"
            />
          </div>

          <div className="flex flex-col gap-6 xl:flex-row">
            <DynamicFormField
              fieldType={FormFieldType.TEXTAREA}
              control={form.control}
              name="familyMedicalHistory"
              label="Family Medical History (if relevant)"
              placeholder="ex: Mother had breast cancer"
            />
            <DynamicFormField
              fieldType={FormFieldType.TEXTAREA}
              control={form.control}
              name="pastMedicalHistory"
              label="Past Medical History"
              placeholder="ex: Asthma diagnosis in childhood"
            />
          </div>
        </section>

        <section className="space-y-4">
          <div className="mb-9 space-y-1">
            <h2 className="sub-header">Identification and Verification</h2>
          </div>
          <DynamicFormField
            fieldType={FormFieldType.SELECT}
            control={form.control}
            name="identificationType"
            label="Identification Type"
            placeholder="Select an option"
          >
            {Object.values(IdentificationTypes).map((idType) => (
              <SelectItem key={idType} value={idType}>
                {idType}
              </SelectItem>
            ))}
          </DynamicFormField>

          <DynamicFormField
            fieldType={FormFieldType.INPUT}
            control={form.control}
            name="identificationNumber"
            label="Identification Number"
            placeholder="ex: 12345678"
          />

          <DynamicFormField
            fieldType={FormFieldType.CUSTOM}
            control={form.control}
            name="identificationDocument"
            label="Scanned Copy of Identification Document"
            renderCustom={(field) => (
              <FormControl>
                <FileUploader files={field.value} onChange={field.onChange} />
              </FormControl>
            )}
          />
        </section>

        <section className="space-y-4">
          <div className="mb-9 space-y-1">
            <h2 className="sub-header">Consent and Privacy</h2>
          </div>

          <DynamicFormField
            fieldType={FormFieldType.CHECKBOX}
            control={form.control}
            name="treatmentConsent"
            label="I consent to receive treatment for my health condition."
          />

          <DynamicFormField
            fieldType={FormFieldType.CHECKBOX}
            control={form.control}
            name="disclosureConsent"
            label="I consent to the use and disclosure of my health information for treatment purposes."
          />

          <DynamicFormField
            fieldType={FormFieldType.CHECKBOX}
            control={form.control}
            name="privacyConsent"
            label="I acknowledge that I have reviewed and agree to the privacy policy."
          />
        </section>

        <SubmitButton isLoading={formSubmitLoading}>
          Submit and Continue
        </SubmitButton>

        {formError && <ErrorPanel error={formError} />}
      </form>
    </Form>
  );
};

export default RegisterForm;
