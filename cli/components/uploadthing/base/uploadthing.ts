import { generateUploadButton, generateUploadDropzone } from '@uploadthing/react';
import { generateReactHelpers } from '@uploadthing/react';

import type {UploadFileRouter} from './core';

export const UploadButton = generateUploadButton<UploadFileRouter>();
export const UploadDropzone = generateUploadDropzone<UploadFileRouter>();

export const {useUploadThing, uploadFiles} = generateReactHelpers<UploadFileRouter>();
