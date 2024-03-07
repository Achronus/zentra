import { FileIcon, X } from 'lucide-react';
import React from 'react'
import { Button } from '../zentra/ui/button';
import { UploadDropzone } from '@/lib/uploadthing';

type Props = {
    apiEndpoint: "media" | "avatar",
    onChange: (url?: string) => void,
    value?: string
}

const FileUpload = ({apiEndpoint, onChange, value}: Props) => {
    const type = value?.split('.').pop();

    if (value) {
        return (
            <div className='flex flex-col justify-center items-center'>
                {type !== "pdf" ? (
                    <div className='relative w-40 h-40'>
                        <img 
                            src={value}
                            alt="Uploaded image"
                            className='object-contain absolute'
                        />
                    </div>
                ) : (
                    <div className='relative flex items-center p-2 mt-2 rounded-md bg-background/10'>
                        <FileIcon/>
                        <a href={value} target="_blank" 
                           rel='noopener_noreferrer' 
                           className='ml-2 text-sm text-indigo-500 dark:text-indigo-400 hover:underline'
                        >
                            View PDF
                        </a>
                    </div>
                )}
                <Button variant="ghost" type="button" onClick={() => onChange('')}>
                    <X className='h-4 w-4'/>
                    Remove Logo
                </Button>
            </div>
        );
    };

    return (
        <div className='w-full bg-muted/30'>
            <UploadDropzone
                endpoint={apiEndpoint}
                onClientUploadComplete={(res) => {onChange(res?.[0].url)}}
                onUploadError={(error: Error) => {console.log(error)}}
            />
        </div>
    )
}

export default FileUpload;
