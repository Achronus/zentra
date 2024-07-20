"use client";

import "react-datepicker/dist/react-datepicker.css";
import "react-phone-number-input/style.css";

import DatePicker from "react-datepicker";
import { Control } from "react-hook-form";
import PhoneInput from "react-phone-number-input";

import { Checkbox } from "@/components/ui/checkbox";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  RadioGroup,
  RadioGroupItem,
} from "@/components/ui/radio-group";
import { Textarea } from "@/components/ui/textarea";
import { Loading } from "@/components/Loading";

import styles from "./form.module.css";
import FileUploader from "./FileUploader";
import {
  FormFieldType,
  ImgDimensions,
  SelectItemType,
} from "./types";
import {
  SelectObjData,
  SelectStrArrayData,
} from "./select";

import Image from "next/image";

type FormProps = {
  control: Control<any>;
  fieldType: FormFieldType;
  name: string;
  label?: string;
  placeholder?: string;
  value?: string;
  iconSrc?: string;
  iconAlt?: string;
  disabled?: boolean;
  dateFormat?: string;
  showTimeSelect?: boolean;
  children?: React.ReactNode;
  defaultCountry?: string;
  data?: SelectItemType[] | string[];
  isLoading?: boolean;
  fileTypes?: string[];
  maxMB?: number;
  maxImgDim?: ImgDimensions;
  renderCustom?: (field: any) => React.ReactNode;
};

type InputFieldProps = {
  field: any;
  iconSrc?: string;
  iconAlt?: string;
  placeholder?: string;
  value?: string;
};

type TextareaProps = {
  field: any;
  placeholder?: string;
  disabled?: boolean;
};

type PhoneFieldProps = {
  field: any;
  placeholder?: string;
  value?: string;
  defaultCountry?: string;
};

type DatePickerProps = {
  field: any;
  iconSrc?: string;
  iconAlt?: string;
  placeholder?: string;
  value?: string;
  dateFormat?: string;
  showTimeSelect?: boolean;
};

type SelectFieldProps = {
  field: any;
  data: SelectItemType[] | string[];
  placeholder?: string;
  value?: string;
  isLoading?: boolean;
};

type CheckboxFieldProps = {
  field: any;
  name: string;
  label?: string;
};

type RadioFieldProps = {
  field: any;
  data: string[];
};

type FileUploadProps = {
  field: any;
  fileTypes?: string[];
  maxMB?: number;
  maxImgDim?: ImgDimensions;
};

const InputField = ({
  field,
  iconSrc,
  iconAlt,
  placeholder,
  value,
}: InputFieldProps) => {
  return (
    <div className={styles.inputContainer}>
      {iconSrc && (
        <Image
          src={iconSrc}
          height={24}
          width={24}
          alt={iconAlt || "icon"}
          className={styles.icon}
        />
      )}
      <FormControl>
        <Input
          placeholder={placeholder}
          {...field}
          className={styles.input}
          value={value ? value : field.value}
        />
      </FormControl>
    </div>
  );
};

const TextareaField = ({
  field,
  placeholder,
  disabled,
}: TextareaProps) => {
  return (
    <FormControl>
      <Textarea
        className={styles.textarea}
        placeholder={placeholder}
        {...field}
        disabled={disabled}
      />
    </FormControl>
  );
};

const PhoneField = ({
  field,
  placeholder,
  value,
  defaultCountry,
}: PhoneFieldProps) => {
  return (
    <FormControl>
      <PhoneInput
        defaultCountry={defaultCountry}
        placeholder={placeholder}
        international
        withCountryCallingCode
        value={value ? value : field.value}
        onChange={field.onChange}
        className={styles.phone}
      />
    </FormControl>
  );
};

const DatePickerField = ({
  field,
  iconSrc,
  iconAlt,
  value,
  showTimeSelect,
  placeholder,
  dateFormat,
}: DatePickerProps) => {
  return (
    <div className={styles.datePickerContainer}>
      {iconSrc && (
        <Image
          src={iconSrc}
          width={24}
          height={24}
          alt={iconAlt || "icon"}
          className={styles.icon}
        />
      )}
      <FormControl>
        <DatePicker
          selected={value ? value : field.value}
          onChange={(date) => field.onChange(date)}
          showTimeSelect={showTimeSelect ?? false}
          dateFormat={dateFormat ?? "dd MMMM yyyy"}
          placeholderText={placeholder}
          timeInputLabel="Time:"
          wrapperClassName={styles.datePicker}
        />
      </FormControl>
    </div>
  );
};

const SelectField = ({
  field,
  value,
  placeholder,
  data,
  isLoading,
}: SelectFieldProps) => {
  const isArrayOfStrings = (
    data: any[]
  ): data is string[] => {
    return data.every((item) => typeof item === "string");
  };

  return (
    <FormControl>
      <Select
        onValueChange={field.onChange}
        defaultValue={value ? value : field.value}
      >
        <FormControl className={styles.selectTrigger}>
          <SelectTrigger>
            <SelectValue placeholder={placeholder} />
          </SelectTrigger>
        </FormControl>
        <SelectContent className={styles.selectContent}>
          {isLoading && !data ? (
            <SelectItem value="loading">
              <Loading width={10} height={10} />
            </SelectItem>
          ) : data && isArrayOfStrings(data) ? (
            <SelectStrArrayData data={data} />
          ) : (
            <SelectObjData data={data} />
          )}
        </SelectContent>
      </Select>
    </FormControl>
  );
};

const CheckboxField = ({
  field,
  name,
  label,
}: CheckboxFieldProps) => {
  return (
    <FormControl>
      <div className={styles.checkboxContainer}>
        <Checkbox
          id={name}
          checked={field.value}
          onCheckedChange={field.onChange}
        />
        <Label
          htmlFor={name}
          className={styles.checkboxLabel}
        >
          {label}
        </Label>
      </div>
    </FormControl>
  );
};

const FileUploadField = ({
  field,
  fileTypes,
  maxMB,
  maxImgDim,
}: FileUploadProps) => {
  return (
    <FormControl>
      <FileUploader
        files={field.value}
        onChange={field.onChange}
        fileTypes={fileTypes}
        maxMB={maxMB}
        maxImgDim={maxImgDim}
      />
    </FormControl>
  );
};

const RadioField = ({ field, data }: RadioFieldProps) => {
  return (
    <FormControl>
      <RadioGroup
        className={styles.radioGroup}
        onValueChange={field.onChange}
        defaultValue={field.value}
      >
        {data.map((option) => (
          <div
            key={option}
            className={styles.radioItemContainer}
          >
            <RadioGroupItem value={option} id={option} />
            <Label
              htmlFor={option}
              className="cursor-pointer"
            >
              {option}
            </Label>
          </div>
        ))}
      </RadioGroup>
    </FormControl>
  );
};

const RenderField = ({
  field,
  props,
}: {
  field: any;
  props: FormProps;
}) => {
  const { fieldType, renderCustom } = props;

  switch (fieldType) {
    case FormFieldType.INPUT:
      return <InputField {...props} />;
    case FormFieldType.TEXTAREA:
      return <TextareaField field={field} {...props} />;
    case FormFieldType.PHONE:
      return <PhoneField field={field} {...props} />;
    case FormFieldType.DATE:
      return <DatePickerField field={field} {...props} />;
    case FormFieldType.SELECT:
      return <SelectField field={field} {...props} />;
    case FormFieldType.CHECKBOX:
      return <CheckboxField field={field} {...props} />;
    case FormFieldType.FILEUPLOAD:
      return <FileUploadField field={field} {...props} />;
    case FormFieldType.RADIO:
      return <RadioField field={field} {...props} />;
    case FormFieldType.CUSTOM:
      return renderCustom ? renderCustom(field) : null;
    default:
      break;
  }
};

const DynamicFormField = (props: FormProps) => {
  const { control, fieldType, name, label } = props;

  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem className={styles.formItem}>
          {fieldType !== FormFieldType.CHECKBOX &&
            label && <FormLabel>{label}</FormLabel>}
          <RenderField field={field} props={props} />

          <FormMessage className={styles.formError} />
        </FormItem>
      )}
    />
  );
};

export default DynamicFormField;
