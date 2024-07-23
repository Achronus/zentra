"use client";

import { ImgDimensions } from "./types";

import { CloudUpload } from "lucide-react";
import Image from "next/image";
import { useCallback } from "react";
import { useDropzone } from "react-dropzone";

type FileUploaderProps = {
  files: File[] | undefined;
  onChange: (files: File[]) => void;
  fileTypes?: string[];
  maxMB?: number;
  maxImgDim?: ImgDimensions;
};

const FileUploader = ({
  files,
  onChange,
  fileTypes = ["SVG", "PNG", "JPG", "PDF"],
  maxMB = 20,
  maxImgDim = { width: 800, height: 400 },
}: FileUploaderProps) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    onChange(acceptedFiles);
  }, []);
  const { getRootProps, getInputProps, isDragActive } =
    useDropzone({ onDrop });

  const formatFileTypes = (fileTypes: string[]): string => {
    const uniqueFileTypes = Array.from(
      new Set(fileTypes)
    ).sort();

    return (
      uniqueFileTypes.slice(0, -1).join(", ") +
      ", or " +
      uniqueFileTypes[uniqueFileTypes.length - 1]
    );
  };

  const convertFileToUrl = (file: File): string =>
    URL.createObjectURL(file);

  return (
    <div
      {...getRootProps()}
      className="file-upload text-12-regular"
    >
      <input {...getInputProps()} />
      {files && files?.length > 0 ? (
        <Image
          src={convertFileToUrl(files[0])}
          width={300}
          height={300}
          alt="uploaded file"
          className="max-h-[400px] overflow-hidden object-cover"
        />
      ) : (
        <>
          <CloudUpload size={40} />
          <div className="file-upload_label">
            {isDragActive ? (
              <p className="text-14-regular transition-all">
                Drop the files here ...
              </p>
            ) : (
              <>
                <p className="text-14-regular transition-all">
                  <span className="text-green-500">
                    Click to upload
                  </span>{" "}
                  or drag and drop
                </p>
                <p>
                  {formatFileTypes(fileTypes)} (
                  {`max
                  ${maxImgDim.width}x${maxImgDim.height}; ${maxMB}MB`}
                  )
                </p>
              </>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default FileUploader;
