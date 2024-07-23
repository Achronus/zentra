import React from "react";
import Image from "next/image";
import { Button } from "@/components//ui/button";
import { UploadDropzone } from "@/lib/uploadthing";
import { FileIcon, X } from "lucide-react";

type FileUploadProps = {
  apiEndpoint: string;
  onChange?: (url?: string) => void;
  value?: string;
};

const FileUpload = ({
  apiEndpoint,
  onChange,
  value,
}: FileUploadProps) => {
  const type = value?.split(".").pop();

  if (value && onChange) {
    return (
      <UploadedFileView
        type={type}
        value={value}
        onChange={onChange}
      />
    );
  }

  if (onChange) {
    return (
      <UploadDropzoneWrapper
        apiEndpoint={apiEndpoint}
        onChange={onChange}
      />
    );
  }

  return (
    <UploadDropzoneWrapper apiEndpoint={apiEndpoint} />
  );
};

const UploadedFileView = ({
  type,
  value,
  onChange,
}: {
  type: string | undefined;
  value: string;
  onChange: (url?: string) => void;
}) => (
  <div className="flex flex-col justify-center items-center">
    {type !== "pdf" ? (
      <ImageView value={value} />
    ) : (
      <PdfView value={value} />
    )}
    <RemoveButton onClick={() => onChange("")} />
  </div>
);

const ImageView = ({ value }: { value: string }) => (
  <div className="relative w-40 h-40">
    <Image
      src={value}
      alt="Uploaded image"
      className="object-contain"
      fill
    />
  </div>
);

const PdfView = ({ value }: { value: string }) => (
  <div className="relative flex items-center p-2 mt-2 rounded-md bg-background/10">
    <FileIcon />
    <a
      href={value}
      target="_blank"
      rel="noopener_noreferrer"
      className="ml-2 text-sm text-indigo-500 dark:text-indigo-400 hover:underline"
    >
      View PDF
    </a>
  </div>
);

const RemoveButton = ({
  onClick,
}: {
  onClick: () => void;
}) => (
  <Button variant="ghost" type="button" onClick={onClick}>
    <X className="h-4 w-4" />
    Remove Logo
  </Button>
);

const UploadDropzoneWrapper = ({
  apiEndpoint,
  onChange,
}: {
  apiEndpoint: string;
  onChange?: (url?: string) => void;
}) => (
  <div className="w-full bg-muted/30">
    <UploadDropzone
      endpoint={apiEndpoint}
      onClientUploadComplete={(res) => {
        onChange
          ? onChange(res?.[0].url)
          : console.log(res);
      }}
      onUploadError={(error: Error) => {
        console.log(error);
      }}
    />
  </div>
);

export { FileUpload };
