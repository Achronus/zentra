export enum FormFieldType {
  INPUT = "input",
  TEXTAREA = "textarea",
  PHONE = "phone",
  CHECKBOX = "checkbox",
  DATE = "date",
  SELECT = "select",
  RADIO = "radio",
  FILEUPLOAD = "fileupload",
  CUSTOM = "custom",
}

export type SelectItemType = {
  name: string;
  imgUrl?: string;
};

export type ImgDimensions = {
  width: number;
  height: number;
};
